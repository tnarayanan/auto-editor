from auto_editor.source.audio_source import AudioSource
from auto_editor.source.audio_params import AudioParams
from auto_editor.analysis.beat_analyzer import BeatAnalyzer
from auto_editor.source.video_source import VideoSource
from auto_editor.source.video_params import VideoParams
from auto_editor.timeline.timeline import Timeline
import numpy as np
import os
import ffmpeg

# file_name, out_name, bpm = "../test_data/oh_the_larceny_another_level_2.wav", "another_level", 145
file_name, out_name, bpm = "../test_data/the_fat_rat_xenogenesis_2.wav", "xenogenesis", 145
# file_name, out_name, bpm = "../test_data/epic_inspiration_ashamaluev_2.wav", "epic_inspiration", 150

audio_source = AudioSource(file_name, AudioParams(bpm=bpm))

video_files_dir = "../test_data/test_video_robot"

input_filenames = []
inputs = []
input_durations = []

for root, dirs, files in os.walk(video_files_dir):
    for filename in files:
        if filename[-4:].lower() == ".mp4":
            input_filenames.append(filename)
            print(filename)

input_filenames.sort()
for filename in input_filenames:
    path = video_files_dir + "/" + filename
    curr = VideoSource(path, VideoParams((1920, 1080), (16, 9), 59.94))
    inputs.append(curr)

audio_source.visualize_signal()

beat_analyzer = BeatAnalyzer(audio_source)
beats = beat_analyzer.analyze()
beats = np.divide(beats, (audio_source.params.sampling_rate / 60))

for i in range(len(beats)):
    beats[i] = int(round(beats[i]))

print("total beats:", len(beats))
print(beats)

timeline = Timeline(inputs, VideoParams((1920, 1080), (16, 9), 59.94), audio_source, beats)
final = timeline.assemble(timeline.split_clips(), "output_test.mp4")
final.run()
