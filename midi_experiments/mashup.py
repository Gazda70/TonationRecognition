import os

from mido import MidiFile
import paths as pth

cv1 = MidiFile(pth.MIDI_FILES + 'new_song.mid', clip=True)
cv3 = MidiFile(pth.MIDI_FILES + 'VampireKillerCV3.mid', clip=True)

del cv1.tracks[4]
del cv1.tracks[4]

cv1.tracks.append(cv3.tracks[4])
cv1.tracks.append(cv3.tracks[5])

cv1.save(pth.MIDI_FILES + 'mashup.mid')
