from mido import MidiFile
import paths as pth
from signature_of_fifths_functions import SignatureOfFifthsUtility

mid = MidiFile(pth.MIDI_FILES + 'VampireKillerCV1.mid', clip=True)
print(mid)
print("MIDI type: " + str(mid.type))

'''
for track in mid.tracks:
    print(track)

for msg in mid.tracks[0]:
    print(msg)
'''
sig_util = SignatureOfFifthsUtility()
print("NUMBER OF TRACKS: " + str(len(mid.tracks)))
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    '''
    for msg in track:
        print(msg)
    '''
for track in mid.tracks:
    print("\n")
    print("TRACK\n")
    print(track)
    print("\n")
    print("NOTES\n")
    notes_dict = sig_util.count_notes_in_track(track)
    for x, y in notes_dict.items():
        print(x, y)
    print("\n")
    '''
    print("MESSAGES")
    print("\n")
    for msg in track:
        print(msg.type)
        print(msg)
    print("\n\n")
    '''