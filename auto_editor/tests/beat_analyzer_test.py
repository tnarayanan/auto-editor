from auto_editor.source.audio_source import AudioSource
from auto_editor.source.audio_params import AudioParams
from auto_editor.analysis.beat_analyzer import BeatAnalyzer
import simpleaudio as sa
import time

# file_name = "../test_data/oh_the_larceny_another_level.wav"
file_name = "../test_data/the_fat_rat_xenogenesis.wav"

source = AudioSource(file_name, AudioParams(bpm=145))

source.visualize_signal()

beat_analyzer = BeatAnalyzer(source)
beats = beat_analyzer.analyze()

wave_obj = sa.WaveObject.from_wave_file(file_name)
frame_time = 1/source.params.sampling_rate

print("total beats:", len(beats))
print(beats)
i = 1

play_obj = wave_obj.play()
print("started playing")
time.sleep((beats[i] * frame_time))
print(i)
while i < len(beats):
    time.sleep((beats[i] - beats[i - 1]) * frame_time)
    i += 1
    print(i)

# if time.time() - start_time > beat_frames[i]*frame_time:
# 	print(i)
# 	# print("beat at", beat_frames[i])
# 	i += 1

print("finished loop at ", time.time())

while play_obj.is_playing():
    continue

print("finished at", time.time())