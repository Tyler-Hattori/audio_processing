import numpy as np

# Calculate average magnitude ratio between source and target notes
def calculate_fft_ratio(source_notes, target_notes):
    # source_notes and target_notes are 2D arrays with shape (number of notes, n_fft)
    # returns the average fft filter calculated across all provided notes
    n_fft = source_notes.shape[1]
    average_fft_ratio = np.zeros((n_fft // 2 + 1,), dtype=complex) # Assume rfft is being used
    for i in range(source_notes.shape[0]):
        source_fft = np.fft.rfft(np.hanning(n_fft) * source_notes[i], n=n_fft)
        target_fft = np.fft.rfft(np.hanning(n_fft) * target_notes[i], n=n_fft)

        fft_ratio = target_fft * np.conj(source_fft) / (np.abs(source_fft)**2 + 1e-8) # Regularized to avoid amplifying noise
        average_fft_ratio += fft_ratio
    return average_fft_ratio /source_notes.shape[0]