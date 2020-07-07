from auto_editor.audio_source import AudioSource

source = AudioSource("../test_data/oh_the_larceny_another_level.wav", 145)

print("getting waveform")
source.get_waveform()