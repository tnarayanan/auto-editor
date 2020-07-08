from auto_editor.source.audio_source import AudioSource
from auto_editor.source.audio_params import AudioParams
from auto_editor.analysis.beat_analyzer import BeatAnalyzer
import time
import numpy as np
import ffmpeg
import sys

sys.setrecursionlimit(10**6)

# file_name, out_name, bpm = "../test_data/oh_the_larceny_another_level_2.wav", "another_level", 145
file_name, out_name, bpm = "../test_data/the_fat_rat_xenogenesis_2.wav", "xenogenesis", 145
# file_name, out_name, bpm = "../test_data/epic_inspiration_ashamaluev_2.wav", "epic_inspiration", 150

source = AudioSource(file_name, AudioParams(bpm=bpm))

source.visualize_signal()

beat_analyzer = BeatAnalyzer(source)
beats = beat_analyzer.analyze()
beats = np.divide(beats, (source.params.sampling_rate / 60))

for i in range(len(beats)):
    beats[i] = int(round(beats[i]))

print("total beats:", len(beats))
print(beats)

audio = ffmpeg.input(file_name)

inputs = []
white_file = ffmpeg.input("../test_data/white.mp4")['v']
black_file = ffmpeg.input("../test_data/black.mp4")['v']

white_file = white_file.split()
black_file = black_file.split()

for i in range(1, len(beats)):
    beats[i] -= 3
    duration = beats[i] - beats[i-1]
    if i % 2 == 1:
        inputs.append(white_file[0].trim(start_frame=0, end_frame=duration))
        white_file = white_file[1].split()
    else:
        inputs.append(black_file[0].trim(start_frame=0, end_frame=duration))
        black_file = black_file[1].split()

joined = None

for i in range(len(inputs)):
    if joined is None:
        print(type(inputs[i]))
        joined = ffmpeg.concat(inputs[i].split()[0])
    else:
        joined = ffmpeg.concat(joined, inputs[i].split()[0])

ffmpeg.output(joined, audio, "beats_" + out_name + ".mp4").run()
