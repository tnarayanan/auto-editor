from auto_editor.source.audio_source import AudioSource
from auto_editor.source.audio_params import AudioParams
from auto_editor.analysis.beat_analyzer import BeatAnalyzer

source = AudioSource("../test_data/the_fat_rat_xenogenesis.wav", AudioParams(145))

print("getting waveform")
print(source.get_signal())
source.visualize_signal()
beat_analyzer = BeatAnalyzer(source)
beat_analyzer.analyze()