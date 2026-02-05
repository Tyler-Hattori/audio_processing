from guitar_processing.utils.estimate_pitch import estimate_pitch
from guitar_processing.utils.calculate_rms import calculate_rms
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt
import numpy as np

def extract_sustained_tones(input_audio, rate, N=1024, hop_length=128, plot=False):
    # Extract segments of length N containing sustained tones from an audio clip

    # Estimate pitch using pYIN and calculate RMS energy
    estimated_f0, voiced_flag, voiced_probs = estimate_pitch(input_audio, rate)
    rms = calculate_rms(input_audio)

    # Calculate local maxima in RMS energy
    peaks, _ = find_peaks(rms, distance=hop_length*2)

    # Calculate RMS energy relative to the most recent previous local maximum
    relative_rms = np.zeros_like(rms)
    current_peak = 1
    for i in range(len(rms)):
        if i in peaks:
            current_peak = rms[i]
        relative_rms[i] = 20 * np.log10(rms[i] / current_peak) if rms[i] != 0 and current_peak > 0 else 0

    # Apply a low pass filter to smooth the relative RMS energy
    smoothed_relative_rms = gaussian_filter1d(relative_rms, sigma=7)

    # Apply a low pass filter to smooth the frequency estimates
    smoothed_estimated_f0 = gaussian_filter1d(estimated_f0, sigma=8)

    # Identify sustained segments
    min_relative_rms_slope = 10 # dB/s
    min_f0_diff = 0.5
    diligence = 5 # number of segments to check forward and back in time
    print(f"Checking for at least {np.round(100 * diligence * N / rate)/100} seconds of sustainability")
    sustained_segments = []
    for i in range(diligence, len(smoothed_relative_rms)-diligence):
        sustained = True
        for j in range(1,diligence):
            if (np.isnan(smoothed_estimated_f0[i-j]) or np.isnan(smoothed_estimated_f0[i+j]) or
                abs(smoothed_estimated_f0[i-j] - smoothed_estimated_f0[i]) > min_f0_diff or
                abs(smoothed_estimated_f0[i] - smoothed_estimated_f0[i+j]) > min_f0_diff):
                sustained = False
                break
            if (smoothed_relative_rms[i] < -10 or
                abs(smoothed_relative_rms[i]-smoothed_relative_rms[i+j]) / (N / rate) > min_relative_rms_slope or
                abs(smoothed_relative_rms[i]-smoothed_relative_rms[i-j]) / (N / rate) > min_relative_rms_slope):
                sustained = False
                break
        if sustained:
            sustained_segments.append(i)

    # Extract audio segments from the identified sustained segments
    sustained_notes = []
    for i in range(len(sustained_segments)):
        start_idx = sustained_segments[i] * hop_length
        end_idx = start_idx + N
        sustained_notes.append(input_audio[start_idx:end_idx])
    sustained_notes = np.array(sustained_notes)

    if plot:
        # Plot Estimated f0 with smoothing
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        for i in range(len(sustained_segments)):
            plt.axvline(x=sustained_segments[i], color='green', linestyle='-', alpha=0.3)
        plt.plot(smoothed_estimated_f0, label='Smoothed Estimated f0 (Hz)', color='blue')
        plt.xlabel('Frame')
        plt.ylabel('Frequency (Hz)')
        plt.title('Smoothed Estimated Fundamental Frequency (f0) over Time')
        plt.legend()

        # Plot RMS energy with smoothing
        plt.subplot(2, 1, 2)
        for i in range(len(sustained_segments)):
            plt.axvline(x=sustained_segments[i], color='green', linestyle='-', alpha=0.3)
        plt.plot(smoothed_relative_rms, label='Smoothed Relative RMS Energy', color='magenta')
        plt.xlabel('Frame')
        plt.ylabel('Relative RMS Energy')
        plt.title('Smoothed Relative RMS Energy over Time')
        plt.legend()
        plt.tight_layout()
        plt.show()

    return sustained_notes # shape: (num_sustained_notes, N)