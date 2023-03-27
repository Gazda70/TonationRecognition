from signature.signature_of_fifths_functions import SignatureOfFifthsUtility
from enum import Enum
import utils.paths as pth
from collections import Counter


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
        self.signature_calculation_mode = SignatureCalculationMode.QUANTITY
        self.base_note = NotesDuration.QUARTER
        self.base_notes_per_tact = self.metrum_numerator * (self.base_note / self.metrum_denominator)

    def get_signature_from_sample_tact_wise(self, tact_number, start_note, end_note):
        pass

    def get_signature_from_sample(self, start_note, end_note):
        notes = {Note.C: 0, Note.C_SHARP: 0, Note.D: 0, Note.D_SHARP: 0, Note.E: 0, Note.F: 0, Note.F_SHARP: 0,
                 Note.G: 0, Note.G_SHARP: 0, Note.A: 0, Note.A_SHARP: 0, Note.B: 0}
        for msg in track:
            if msg.is_cc():
                if msg.type == 'note_on':
                    notes[Note(msg.note % 12)] += 1
        return notes



class Track:
    def __init__(self, track, activated=False, number=0):
        self.track = track
        self.activated = activated
        self.number = number
        self.window_start = 0
        self.window_end = 0

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

    def set_window(self, start, end):
        self.window_start = start
        self.window_end = end

    def get_notes_from_window(self):
        if self.track is not [] and self.window_start >= 0 and self.window_end < len(self.track):
            to_return = self.track[self.window_start:self.window_end]
            print(to_return)
            return to_return




class TrackManager:
    def __init__(self):
        self.tracks = []
        self.track_count = 0

    def process_file(self, midi_file):
        print(midi_file)
        print("MIDI type: " + str(midi_file.type))
        print("NUMBER OF TRACKS: " + str(len(midi_file.tracks)))
        for i, track in enumerate(midi_file.tracks):
            print('Track {}: {}'.format(i, track.name))
        for i, track in enumerate(midi_file.tracks):
            print("\n")
            print("TRACK\n")
            print(track)
            print("\n")
            print("NOTES\n")
            self.tracks.append(Track(track, activated=False, number=i))
        self.track_count = len(midi_file.tracks)

    def activate_track(self, track_number):
        if track_number < self.track_count:
            self.tracks[track_number].activate()

    def deactivate_track(self, track_number):
        if track_number < self.track_count:
            self.tracks[track_number].deactivate()

    def handle_selection(self, track_number):
        if (self.tracks[track_number].activated is True):
            self.tracks[track_number].deactivate()
        else:
            self.tracks[track_number].activate()

    def is_track_selected(self, track_number):
        return self.tracks[track_number].activated

    def calculate_signature(self):
        sig_util = SignatureOfFifthsUtility()
        notes_dict = sig_util.initialize_empty_notes_dict()
        for track in self.tracks:
            if track.activated is True:
                notes_dict += sig_util.count_notes_in_track(track.track)

        signature = sig_util.calculate_signature_of_fifths(notes_dict)
        print("NOTES DICT: ")
        for x, y in notes_dict.items():
            print(x, y)
        print("SIGNATURE DICT: ")
        for x, y in signature.signature.items():
            print(x, y)
        print("\n")
        return signature
