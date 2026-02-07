import numpy as np
import sys
import IPython.display as ipd
from scipy.io.wavfile import read

# Normalized LMS Adaptive Filter
def cancel_noise(noisy_input, reference_noise, rate=44100, num_taps=64, learning_rate=0.01):
    N = len(reference_noise) # Should be the same as len(noisy_input)
    eps = 1e-6 # Small constant to avoid division by zero
    w_prev = np.zeros(num_taps) # Initial weights
    w = np.zeros((N, num_taps)) # To store weights over time
    e = np.zeros(N) # Error signal

    # Run the filter
    for n in range(num_taps, N):
        x_n = reference_noise[n - num_taps:n][::-1] # Input vector (most recent samples)
        y_n = np.dot(w_prev, x_n) # Filter output
        e[n] = input[n] - y_n # Error signal
        w_new = w_prev + learning_rate * e[n] * x_n / (np.dot(x_n, x_n) + eps) # Update weights
        w[n, :] = w_new
        w_prev = w_new
    
    return e, w

if __name__ == "main":
    num_taps = 64
    learning_rate = 0.01
    if len(sys.argv) < 3:
        raise Exception("Input a path to a noisy signal and a path to a signal with correlated noise\nOptionally, enter num_taps, learning_rate")
    if len(sys.argv) >= 3:
        num_taps = sys.argv[3]
    if len(sys.argv) >= 4:
        learning_rate = sys.argv[4]
    
    input_audio_path = sys.argv[1]
    noise_audio_path = sys.argv[2]

    # Load audio clips
    rate, input_audio = read(input_audio_path)
    rate, noise_audio = read(noise_audio_path)

    # Convert to mono if stereo
    if input_audio.ndim > 1:
        input_audio = input_audio.mean(axis=1).astype(input_audio.dtype)
    if noise_audio.ndim > 1:
        noise_audio = noise_audio.mean(axis=1).astype(noise_audio.dtype)

    # Convert to floating point and normalize
    input_audio = input_audio.astype(np.float32) / np.max(np.abs(input_audio))
    noise_audio = noise_audio.astype(np.float32) / np.max(np.abs(noise_audio))

    # Apply filter
    cleaned_audio, weights = cancel_noise(input_audio, noise_audio, rate, num_taps, learning_rate)

    # Play audio
    ipd.display(ipd.Audio(cleaned_audio, rate=rate))
    