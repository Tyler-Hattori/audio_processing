import numpy as np

def detect_onsets(rms, threshold=0.1):
    # Returns indeces of peaks in the rms array above a given threshold
    onsets = []
    for i in range(1,len(rms)-1): 
        if rms[i] - rms[i-1] > 0 and rms[i+1] - rms[i] < 0 and rms[i] > threshold: 
            onsets += [i] 
    return np.array(onsets)