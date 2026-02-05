import librosa

def calculate_rms(clip, frame_length=N, hop_length=hop_length):
    # Calculate the RMS energy of an audio clip at given frame and hop lengths
    rms = librosa.feature.rms(y=clip, frame_length=frame_length, hop_length=hop_length)[0]
    return rms # Return RMS energy as a 1D numpy array