import numpy as np
import matplotlib.pyplot as plt
from guitar_processing.scripts.extract_sustained_tones import extract_sustained_tones
from guitar_processing.utils.calculate_fft_ratio import calculate_fft_ratio
from guitar_processing.utils.apply_fft_filter import apply_filter
import IPython.display as ipd

def replicate_timbre(input_audio, source_clip, target_clip, rate, N, hop_length, plot=False, play_audio=True):
    
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

    # Play the output audio
    if play_audio:
        ipd.display(ipd.Audio(output_audio, rate=rate))

    return output_audio


