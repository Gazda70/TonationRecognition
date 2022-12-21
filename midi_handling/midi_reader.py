from enum import Enum

from mido import MidiFile
import utils.paths as pth
from signature.signature_of_fifths_functions import SignatureOfFifthsUtility

class SignatureCalculationMode(Enum):
    QUANTITY, DURATION = range(2)

class NotesDuration(Enum):
    WHOLE=1
    HALF=2
    QUARTER=4
    EIGHT=8
    SIXTEEN=16
    THIRTY_TWO=32
    SIXTY_FOUR=64

class MidiSample:
    def __init__(self):
        self.metrum_numerator = 4
        self.metrum_denominator = NotesDuration.QUARTER
        self.file = None
        self.signature_calculation_mode = SignatureCalculationMode.QUANTITY
        self.base_note = NotesDuration.QUARTER
        self.base_notes_per_tact = self.metrum_numerator * (self.base_note / self.metrum_denominator)

    def get_signature_from_sample_tact_wise(self, tact_number, start_note, end_note):
        pass

    def get_signature_from_sample(self, start_note, end_note):
        pass
class MidiReader:

    def read_file(self, midi_path):
        self.midi_file = MidiFile(midi_path, clip=True)
        signatures_per_track = []

        # print(self.midi_file)
        # print("MIDI type: " + str(self.midi_file.type))
        sig_util = SignatureOfFifthsUtility()
        print("NUMBER OF TRACKS: " + str(len(self.midi_file.tracks)))
        for i, track in enumerate(self.midi_file.tracks):
            print('Track {}: {}'.format(i, track.name))
        for track in self.midi_file.tracks:

            # print("\n")
            # print("TRACK\n")
            # print(track)
            # print("\n")
            # print("NOTES\n")

            notes_dict = sig_util.count_notes_in_track(track)

            print("NOTES DICT: ")
            for x, y in notes_dict.items():
                print(x, y)

            signature = sig_util.calculate_signature_of_fifths(notes_dict)
            signatures_per_track.append(signature)

            print("SIGNATURE DICT: ")
            for x, y in signature.signature.items():
                print(x, y)
            print("\n")


        return signatures_per_track