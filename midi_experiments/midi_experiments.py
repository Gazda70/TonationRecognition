from mido import MidiFile

MIDI_FILES = "E:\PracaMagisterska\TonationRecognition\midi_files\\"
mid = MidiFile(MIDI_FILES + 'VampireKillerCV1.mid', clip=True)
print(mid)