from enum import Enum

from mido import MidiFile
import utils.paths as pth
from midi_handling.track_manager import TrackManager

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
        self.metrum_numerator = NotesDuration.QUARTER
        self.metrum_denominator = NotesDuration.QUARTER
        self.file = None
        self.signature_calculation_mode = SignatureCalculationMode.QUANTITY
        self.base_note = NotesDuration.QUARTER
        self.base_notes_per_tact = self.metrum_numerator * (self.base_note / self.metrum_denominator)

    def get_signature_from_sample_tact_wise(self, tact_number, start_note, end_note):
        pass

    def get_signature_from_sample(self, start_note, end_note):
        #start_note =
        msg_types = []
        notes = {Note.C: 0, Note.C_SHARP: 0, Note.D: 0, Note.D_SHARP: 0, Note.E: 0, Note.F: 0, Note.F_SHARP: 0,
                 Note.G: 0, Note.G_SHARP: 0, Note.A: 0, Note.A_SHARP: 0, Note.B: 0}
        for msg in track:
            if msg.is_cc():
                print("CONTROL MESSAGE")
                print(msg)
            if msg.type == 'note_on':
                notes[Note(msg.note % 12)] += 1
        # print("MESSAGE TYPES: " + str(Counter(msg_types).keys()))
        # print("MESSAGE TYPES OCCURRENCE FREQUENCY: " + str(Counter(msg_types).values()))
        return notes
        pass


class MidiReader:

    def read_file(self, midi_path):
        print("read file")
        self.midi_file = MidiFile(midi_path, clip=True)
        track_manager = TrackManager()
        track_manager.process_file(self.midi_file)

        return track_manager