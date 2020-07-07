class AudioParams:
    def __init__(self, bpm: int):
        self.bpm: int = bpm
        self.sampling_rate: int = 0 # set when attached to audio source
