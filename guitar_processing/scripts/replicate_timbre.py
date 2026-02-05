import numpy as np
import matplotlib.pyplot as plt
from guitar_processing.scripts.extract_sustained_tones import extract_sustained_tones

def replicate_timbre(input_audio, source_clip, target_clip, rate, N, hop_length, plot=False):
    
    # Extract sustained notes from source and target clips
    source_notes = extract_sustained_tones(source_clip, rate, N, hop_length, plot=plot)
    target_notes = extract_sustained_tones(target_clip, rate, N, hop_length, plot=plot)
    print(f"Extracted {len(source_notes)} source notes and {len(target_notes)} target notes")

    # Calculate average regularized FFT ratio between target and source notes
    average_fft_ratio = np.zeros(N//2 + 1, dtype=complex)
    for i in range(min(len(source_notes), len(target_notes))):
        source_fft = np.fft.rfft(np.hanning(N) * source_notes[i], n=N)
        target_fft = np.fft.rfft(np.hanning(N) * target_notes[i], n=N)

        fft_ratio = target_fft * np.conj(source_fft) / (np.abs(source_fft)**2 + 1e-8)
        average_fft_ratio += fft_ratio
    average_fft_ratio /= min(len(source_notes), len(target_notes))
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

    if N < 2048:
        # Implement the filter in real time using overlap-add method
        output_audio = np.zeros_like(input_audio)
        window = np.hanning(N)
        filter = average_fft_ratio
        for start in range(0, len(input_audio) - N + 1, hop_length):
            end = start + N
            input_segment = input_audio[start:end]
            input_fft = np.fft.rfft(window * input_segment, n=N)
            modified_fft = input_fft * filter
            modified_segment = np.fft.irfft(modified_fft, n=N)
            output_audio[start:end] += window * modified_segment
        print("Applied filter in real time using overlap-add method")
    else:
        # Implement the filter as a partitioned convolution in the time domain
        filter = np.fft.irfft(average_fft_ratio, n=N)
        block_size = 128
        filters = np.array_split(filter, len(filter) // block_size)
        fft_filters = np.fft.fft(filters)
        for start in range(0, len(input_audio) - N + 1, hop_length):
            end = start + N
            input_segment = input_audio[start:end]
            # zero padd input
            
            input_fft = 



