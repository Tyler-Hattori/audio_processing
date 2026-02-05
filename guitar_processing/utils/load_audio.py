from scipy.io.wavfile import read
import numpy as np

def load_audio(path):
    rate, input = read(path)

    # Convert to mono if stereo
    if input.ndim > 1:
        input = input.mean(axis=1).astype(input.dtype)

    # Convert to floating point and normalize
    input = input.astype(np.float32) / np.max(np.abs(input))

    return rate, input