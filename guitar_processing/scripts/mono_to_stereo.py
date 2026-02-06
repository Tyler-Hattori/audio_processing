import numpy as np
from scipy.io.wavfile import read
from guitar_processing.utils.calculate_path_loss import path_loss_dB
import IPython.display as ipd
import sys

# Assume the listener is at the origin
# Distance measured in meters
# Distance between the ears is about 0.15 meters
def mono_to_stereo(audio, rate, init_coords=[0,0], velocity=[0,0]):
    # If stereo convert to mono
    if audio.ndim > 1:
        audio = audio.mean(axis=1).astype(audio.dtype)
    N = len(audio)
    n_fft = 1024
    time = np.arange(0, (N+n_fft)/rate, 1/rate) # seconds
    head_width = 0.15 # meters

    # Calculate source positions and distance over time
    x_coords = init_coords[0] + velocity[0] * time
    y_coords = init_coords[1] + velocity[1] * time
    distances_left = np.sqrt((x_coords + head_width / 2)**2 + y_coords**2)
    distances_right = np.sqrt((x_coords - head_width / 2)**2 + y_coords**2)
    
    # Calculate delays to each ear
    delays_left = distances_left / speed_of_sound
    delays_right = distances_right / speed_of_sound

    # Apply frequency-dependent path loss in the frequency domain
    window = np.hanning(n_fft)
    output_left = np.zeros(len(time))
    output_right = np.zeros(len(time))
    hop_length = n_fft // 4

    # Specify frequency domain coefficients for a low pass filter to apply when sounds are behind the listener
    freqs = np.fft.rfftfreq(n_fft, d=1/rate)
    start_decay_idx = int(1000 * (len(freqs) - 1) / (rate/2)) # The human hearing low pass filter takes noticeable effect around 1.5kHz
    end_decay_idx = int(3000 * (len(freqs) - 1) / (rate/2))
    low_pass = np.zeros_like(freqs)
    low_pass[:start_decay_idx] = 1
    low_pass[start_decay_idx:end_decay_idx] = [1 - (i-start_decay_idx)/(end_decay_idx - start_decay_idx) for i in range(start_decay_idx, end_decay_idx)]

    # Apply the delays and attenuations in the frequency domain
    for start_idx in range(0, N - n_fft, hop_length):
        # Calculate FFT of input block
        block = audio[start_idx:start_idx + n_fft] * window
        X = np.fft.rfft(block)

        # Apply delay via phase shift
        X_left = X * np.exp(-1j * 2 * np.pi * freqs * delays_left[start_idx]) 
        X_right = X * np.exp(-1j * 2 * np.pi * freqs * delays_right[start_idx])

        # Apply path loss
        X_left = X_left * 10**(-(path_loss_dB(distances_left[start_idx], freqs) / 20))
        X_right = X_right * 10**(-(path_loss_dB(distances_right[start_idx], freqs) / 20))

        # Apply a low pass filter if the sound is behind the listener
        if y_coords[start_idx] < 0:
            X_left *= low_pass
            X_right *= low_pass

        # Recontruct in the time domain
        block_left = np.fft.irfft(X_left) * window 
        block_right = np.fft.irfft(X_right) * window 

        output_left[start_idx:start_idx + n_fft] += block_left
        output_right[start_idx:start_idx + n_fft] += block_right

    return [output_left, output_right]

if __name__ == "__main__":
    x_init = 0
    y_init = 0
    x_vel = 0
    y_vel = 0
    if len(sys.argv) == 1:
        raise Exception("Input the path to an audio file.\nOptionally, add x_init, y_init, x_velocity, y_velocity")
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
    if len(sys.argv) > 2:
        x_init = sys.argv[2]
    if len(sys.argv) > 3:
        y_init = sys.argv[3]
    if len(sys.argv) > 4:
        x_vel = sys.argv[4]
    if len(sys.argv) > 5:
        y_vel = sys.argv[5]

    # Load audio clip
    rate, audio = read(audio_path)

    # Convert to mono if stereo
    if audio.ndim > 1:
        audio = audio.mean(axis=1).astype(audio.dtype)

    # Convert to floating point and normalize
    audio = audio.astype(np.float32) / np.max(np.abs(audio))

    # Convert to stereo
    print("Converting to stereo...")
    stereo_audio = mono_to_stereo(audio, rate, init_coords=[x_init,y_init], velocity=[x_vel,y_vel])

    # Play audio
    print("Playing stereo audio...")
    ipd.display(ipd.Audio(stereo_audio, rate=rate, normalize=False))   