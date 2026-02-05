import numpy as np

# Overlap-add FFT convolution method
def apply_filter(freq_filter, x, n_fft=None):
    # freq_filter: frequency response from np.fft.rfft (length = n_fft//2 + 1)
    # x: 1D time-domain input (float)
    if n_fft is None:
        n_fft = (len(freq_filter) - 1) * 2
    N = n_fft
    if len(freq_filter) != N // 2 + 1:
        raise ValueError("freq_filter length must equal n_fft//2 + 1 (rfft bins)")
    hop = N // 4
    win = np.hanning(N)
    out = np.zeros(len(x) + N, dtype=np.float32)

    for start in range(0, len(x), hop):
        chunk = x[start:start+N]
        if len(chunk) < N:
            chunk = np.pad(chunk, (0, N - len(chunk)))
        chunk_win = chunk * win
        chunk_fft = np.fft.rfft(chunk_win, n=N)
        modified_fft = chunk_fft * freq_filter
        modified = np.fft.irfft(modified_fft, n=N)
        out[start:start+N] += modified * win

    return out[:len(x)]