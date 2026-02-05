import librosa
def estimate_pitch(clip, rate, fmin=70, fmax=1047):
    f0, voiced_flag, voiced_probs = librosa.pyin(clip, fmin=fmin, fmax=fmax, sr=rate, frame_length=N, hop_length=hop_length)
    return f0, voiced_flag, voiced_probs