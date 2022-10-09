from mido import MidiFile
from functions import paths as pth

cv1 = MidiFile(pth.MIDI_FILES + 'VampireKillerCV1.mid', clip=True)

message_numbers = []
duplicates = []

for track in cv1.tracks:
    if len(track) in message_numbers:
        duplicates.append(track)
    else:
        message_numbers.append(len(track))

for track in duplicates:
    cv1.tracks.remove(track)

cv1.save(pth.MIDI_FILES + 'new_song.mid')
