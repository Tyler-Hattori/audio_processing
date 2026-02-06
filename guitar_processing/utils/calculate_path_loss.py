import numpy as np

# Free space path loss for audible frequencies
def path_loss_dB(distance, freqs):
    speed_of_sound = 343 # meters per second, constant for audible frequencies
    return 20*np.log10(max(distance,0.1)) + 20*np.log10([max(f,1) for f in freqs]) + 20 * np.log10(4*np.pi/speed_of_sound)