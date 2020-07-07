import wave
import numpy as np


class AudioSource:
    def __init__(self, audio_path: str, bpm: int):
        self.audio_path = audio_path
        self.bpm = bpm

        self.audio = wave.open(self.audio_path, 'r')
        self.sampling_rate = self.audio.getframerate()

    def get_waveform(self) -> list:
        signal = self.audio.readframes(-1)
        signal = np.frombuffer(signal, dtype='int16')
        signal = signal[1::2]

        print(type(signal))

        return signal
