from mido import MidiFile
import utils.paths as pth
from signature.signature_of_fifths_functions import SignatureOfFifthsUtility


class MidiReader:
    def read_file(self, midi_path):
        self.midi_file = MidiFile(midi_path, clip=True)

        mid = MidiFile(pth.MIDI_FILES + 'VampireKillerCV1.mid', clip=True)
        print(mid)
        print("MIDI type: " + str(mid.type))
        sig_util = SignatureOfFifthsUtility()
        print("NUMBER OF TRACKS: " + str(len(mid.tracks)))
        for i, track in enumerate(mid.tracks):
            print('Track {}: {}'.format(i, track.name))
        for track in mid.tracks:
            print("\n")
            print("TRACK\n")
            print(track)
            print("\n")
            print("NOTES\n")
            notes_dict = sig_util.count_notes_in_track(track)
            print("NOTES DICT: ")
            for x, y in notes_dict.items():
                print(x, y)
            signature = sig_util.calculate_signature_of_fifths(notes_dict)
            print("SIGNATURE DICT: ")
            for x, y in signature.signature.items():
                print(x, y)
            print("\n")