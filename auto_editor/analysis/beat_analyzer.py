from auto_editor.source.audio_source import AudioSource
import numpy as np
import matplotlib.pyplot as plt

class BeatAnalyzer:
    def __init__(self, source: AudioSource):
        self.source: AudioSource = source

    def analyze(self, *args):
        return self.analyze_simple_on_beat(*args)

    def analyze_average_subdivisions(self, beat_threshold: float = 0.13) -> np.ndarray:
        modified_signal = []
        samples_per_beat = 60 * self.source.params.sampling_rate // self.source.params.bpm
        beat_subdivisions = 50
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

    def analyze_simple(self, beat_threshold: float = 0.53) -> np.ndarray:
        beat_frames = [0]
        samples_per_beat = 60 * self.source.params.sampling_rate / self.source.params.bpm
        difference = samples_per_beat
        for i in range(1, len(self.source.signal)):
            if i - beat_frames[len(beat_frames) - 1] > difference and abs(self.source.signal[i]) > beat_threshold:
                beat_frames.append(i)

        return np.array(beat_frames)

    def analyze_simple_on_beat(self, beat_threshold: float = 0.53) -> np.ndarray:
        beat_frames = [0]
        samples_per_beat = int(60 * self.source.params.sampling_rate / self.source.params.bpm)
        window_width = samples_per_beat//3

        for i in range(samples_per_beat, len(self.source.signal), samples_per_beat):
            if np.max(np.abs(self.source.signal[i-window_width//2:i+window_width//2])) > beat_threshold:
                beat_frames.append(i)
            # beat_frames.append(i)

        return np.array(beat_frames)

    # Sound analyzer algorithm
    def analyze_energies(self) -> np.ndarray:
        beats = []

        block_size = 8192
        energies = []
        for i in range(len(self.source.signal) // block_size):
            s = 0
            for j in range(i*block_size, (i+1)*block_size):
                s += (self.source.signal[j] ** 2)
            energies.append(s)

        energies = np.array(energies)
        # print(len(energies))

        blocks_per_second = self.source.params.sampling_rate // block_size

        for i in range(0, len(energies) - blocks_per_second + 1, blocks_per_second):
            avg_e = np.mean(energies[i:i+blocks_per_second])
            var_e = np.var(energies[i:i+blocks_per_second])
            # C = -0.00015 * var_E + 1.5142857
            C = -0.000015 * var_e + 2.8142857

            for j in range(i, i+blocks_per_second):
                if energies[j] > C * avg_e:
                    beats.append(j*block_size)
                    print("BEAT: var= ", var_e, " C= ", C, " avg= ", avg_e, " E= ", energies[j], " j= ", j)

        return np.array(beats)

    def analyze_scaled_segments(self, beat_threshold: float = 0.95) -> np.ndarray:
        scaled_signal = np.copy(self.source.signal)
        block_size = self.source.params.sampling_rate

        for i in range(len(self.source.signal) // block_size):
            s = i*block_size
            e = (i+1)*block_size
            scaled_signal[s:e] = scaled_signal[s:e] / np.max(np.abs(scaled_signal[s:e]))
            # scaled_signal[s:e] *= (1 / scaled_signal[s:e].max())

        print(len(scaled_signal))

        time_axis = np.linspace(0, len(scaled_signal) / self.source.params.sampling_rate, num=len(scaled_signal))

        plt.figure(1)
        plt.title("Scaled Signal Wave...")
        plt.plot(time_axis, scaled_signal)
        plt.show()

        beat_frames = [0]
        samples_per_beat = 60 * self.source.params.sampling_rate / self.source.params.bpm
        for i in range(1, len(scaled_signal)):
            if i - beat_frames[len(beat_frames) - 1] > samples_per_beat and abs(scaled_signal[i]) > beat_threshold:
                beat_frames.append(i)
                i += samples_per_beat

        return np.array(beat_frames)
