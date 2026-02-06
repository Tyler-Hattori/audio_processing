import numpy as np
import matplotlib.pyplot as plt
from guitar_processing.scripts.extract_sustained_tones import extract_sustained_tones
from guitar_processing.utils.calculate_fft_ratio import calculate_fft_ratio
from guitar_processing.utils.apply_fft_filter import apply_filter
import IPython.display as ipd
from scipy.io.wavfile import read
import IPython.display as ipd
import sys

def replicate_timbre(input_audio, source_clip, target_clip, rate, N, hop_length, plot=False):
    # Extract sustained notes from source and target clips
    source_notes = extract_sustained_tones(source_clip, rate, N, hop_length, plot=plot)
    target_notes = extract_sustained_tones(target_clip, rate, N, hop_length, plot=plot)
    print(f"Extracted {len(source_notes)} source notes and {len(target_notes)} target notes")

    # Calculate average regularized FFT ratio between target and source notes
    average_fft_ratio = calculate_fft_ratio(source_notes, target_notes)
    print("Calculated average FFT ratio between target and source notes")

    if plot:
        # Plot the average magnitude ratios
        frequencies = np.fft.rfftfreq(N, d=1/rate)
        plt.figure(figsize=(12, 3))
        plt.plot(frequencies, np.abs(average_fft_ratio), label='Average FFT Ratio Magnitude')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.title('Average FFT Ratio Magnitude')
        plt.legend()
        plt.show()

    # Apply the filter using the overlap-add method
    output_audio = apply_filter(average_fft_ratio, input_audio)

    return output_audio

if __name__ == "__main__":
    N = 0
    hop_length = 0
    plot = False
    if len(sys.argv) < 4:
        raise Exception("Input the path to an audio file to be converted, the path to a source audio, and the path to a target audio to mimic.\nOptionally, add window_length, hop_length, show_plots")
    if len(sys.argv) >= 4:
        N = sys.argv[4]
    if len(sys.argv) >= 5:
        hop_length = sys.argv[5]
    if len(sys.argv) >= 6:
        plot = sys.argv[6]

    input_audio_path = sys.argv[1]
    source_audio_path = sys.argv[2]
    target_audio_path = sys.argv[3]

    # Load audio clips
    rate, input_audio = read(input_audio_path)
    rate, source_audio = read(source_audio_path)
    rate, target_audio = read(target_audio_path)

    # Convert to mono if stereo
    if input_audio.ndim > 1:
        input_audio = input_audio.mean(axis=1).astype(input_audio.dtype)

    # Convert to floating point and normalize
    input_audio = input_audio.astype(np.float32) / np.max(np.abs(input_audio))

    # Convert the input audio timbre to what is contained in the target clip
    output_audio = replicate_timbre(input_audio, source_audio, target_audio, rate, N, hop_length, plot)

    # Play the output audio
    ipd.display(ipd.Audio(output_audio, rate=rate))