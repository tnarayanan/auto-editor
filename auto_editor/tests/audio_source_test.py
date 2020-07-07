from auto_editor.source.audio_source import AudioSource

source = AudioSource("../test_data/oh_the_larceny_another_level.wav", 145)

print("getting waveform")
print(source.get_waveform())