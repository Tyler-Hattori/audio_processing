import IPython.display as ipd

def play_audio(clip, rate=44100):
    ipd.display(ipd.Audio(clip, rate=rate))