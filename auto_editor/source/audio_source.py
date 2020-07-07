import wave
import numpy as np
import matplotlib.pyplot as plt
from auto_editor.source.audio_params import AudioParams


class AudioSource:
    def __init__(self, audio_path: str, params: AudioParams):
        self.audio_path = audio_path
        self.params = params

        self.audio = wave.open(self.audio_path, 'r')
        self.params.sampling_rate = self.audio.getframerate()
        print("sampling rate: ", self.params.sampling_rate)

        self.signal = self.get_signal()

    def get_signal(self) -> np.ndarray:
        signal = self.audio.readframes(-1)
        signal = np.frombuffer(signal, dtype='int16')
        signal = signal[1::2]

        return signal

    def visualize_signal(self):
        print(len(self.signal))

        time_axis = np.linspace(0, len(self.signal) / self.params.sampling_rate, num=len(self.signal))

        plt.figure(0)
        plt.title("Original Signal Wave...")
        plt.plot(time_axis, self.signal)
        plt.show()
