from mido import MidiFile
import paths as pth


mid = MidiFile(pth.MIDI_FILES + 'VampireKillerCV1.mid', clip=True)
print(mid)

for track in mid.tracks:
    print(track)

for msg in mid.tracks[0]:
    print(msg)

for track in mid.tracks:
    print("TRACK\n")
    print(track)
    print("\n")
    print("MESSAGES")
    print("\n")
    for msg in track:
        print(msg)
    print("\n\n")