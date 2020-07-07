from auto_editor.source.audio_source import AudioSource
import numpy as np
import matplotlib.pyplot as plt


class BeatAnalyzer:
    def __init__(self, source: AudioSource):
        self.source: AudioSource = source

    def analyze(self, beat_threshold: int = 80) -> np.ndarray:
        modified_signal = []
        samples_per_beat = 60 * self.source.params.sampling_rate // self.source.params.bpm
        beat_subdivisions = 4
        group_size = samples_per_beat // beat_subdivisions

        for i in range(len(self.source.signal) // group_size):
            modified_signal.append(np.mean(self.source.signal[i * group_size : (i + 1) * group_size]))

        time_axis = np.linspace(0, len(modified_signal) / self.source.params.sampling_rate, num=len(modified_signal))

        plt.figure(1)
        plt.title("Modified Signal Wave...")
        plt.plot(time_axis, modified_signal)
        plt.show()

        # analyze the signal to get the beat frames

        beat_frames = [0]
        for i in range(1, len(modified_signal)):
            if i - beat_frames[len(beat_frames) - 1] > beat_subdivisions and abs(modified_signal[i]) > beat_threshold:
                beat_frames.append(i)

        # beat_frames = [x - 4*44100/30 for x in beat_frames]
        return np.multiply(np.array(beat_frames), group_size)
