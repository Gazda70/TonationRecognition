from signature.signature_of_fifths_functions import SignatureOfFifthsUtility, Note
from enum import Enum
import utils.paths as pth
from collections import Counter
from dataclasses import dataclass
from mido import second2tick

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

class SignatureModes(Enum):
    QUANTITY=1
    DURATION=2
'''
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
'''

class RhytmicValues(Enum):
    WHOLE=1
    HALF=2
    QUARTER=4
    EIGHT=8
    SIXTEEN=16
    THIRTY_TWO=32
    SIXTY_FOUR=64

@dataclass
class RhytmicValuesDuration:
    WHOLE: int
    HALF: int
    QUARTER: int
    EIGHT: int
    SIXTEEN: int
    THIRTY_TWO: int
    SIXTY_FOUR: int

@dataclass
class ProcessedElement:
    is_chord: bool
    notes: []

@dataclass
class NoteWithDuration:
    note: Note
    duration: RhytmicValues

@dataclass
class ProcessedTrack:
    elements: []


class Track:
    def __init__(self, notes_quantity, minimum_rhytmic_value=float('inf'),
                 tempo=500000, activated=False, number=0):
        self.messages = []
        self.activated = activated
        self.number = number
        self.window_start = 0
        self.window_end = 0
        self.notes_quantity = notes_quantity
        self.minimum_rhytmic_value = minimum_rhytmic_value
        self.tempo = tempo

    def extract_note_messages_quantity(self, start_time_point, end_time_point):
        messages = self.get_messages_from_window(start_time_point, end_time_point)
        notes = Counter({Note.C: 0, Note.C_SHARP: 0, Note.D: 0, Note.D_SHARP: 0, Note.E: 0, Note.F: 0, Note.F_SHARP: 0,
                 Note.G: 0, Note.G_SHARP: 0, Note.A: 0, Note.A_SHARP: 0, Note.B: 0})
        print("Notes window")
        print(messages)
        for msg in messages:
            notes[Note(msg.note % 12)] += 1

        print("Notes dictionary: ")
        print(notes)
        return notes

    def extract_note_messages_duration(self, start_time_point, end_time_point):
        messages = self.get_messages_from_window(start_time_point, end_time_point)
        notes = Counter({Note.C: 0, Note.C_SHARP: 0, Note.D: 0, Note.D_SHARP: 0, Note.E: 0, Note.F: 0, Note.F_SHARP: 0,
                 Note.G: 0, Note.G_SHARP: 0, Note.A: 0, Note.A_SHARP: 0, Note.B: 0})
        print("Notes window")
        print(messages)
        for msg in messages:
            notes[Note(msg.note % 12)] += msg.time

        print("Notes dictionary: ")
        print(notes)
        return notes

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

    def set_window(self, start, end):
        self.window_start = start
        self.window_end = end

    def get_messages_from_window(self, start_time_point, end_time_point):
        passed_time = 0
        messages_to_return = []
        for msg in self.messages:
            passed_time += start.time
            passed_time += end.time
            if passed_time >= end_time_point:
                break
            if start_time_point < passed_time:
                messages_to_return.append(end)
        print('Messages to return from track {}'.format(self.number))
        print(*messages_to_return)
        return messages_to_return


class TrackManager:
    def __init__(self):
        self.raw_tracks = []
        self.processed_tracks = []
        self.track_count = 0
        self.notes_quantity = 0
        self.total_time = 0
        self.minimum_rhytmic_value = float('inf')
        self.tempo = 0
        self.rhytmic_values_duration = RhytmicValuesDuration(2000000, 1000000, 500000, 250000, 125000, 62500, 31250)
        self.ticks_per_beat = 0

    def process_file(self, midi_file):
        # print(midi_file)
        # print("MIDI type: " + str(midi_file.type))
        # print("NUMBER OF TRACKS: " + str(len(midi_file.tracks)))
        # for i, track in enumerate(midi_file.tracks):
        #     print('Track {}: {}'.format(i, track.name))
        print("MIDI type: " + str(midi_file.type))
        print("Playback time: " + str(midi_file.length))
        print("Ticks per beat: " + str(midi_file.ticks_per_beat))
        self.ticks_per_beat = midi_file.ticks_per_beat
        self.total_time = midi_file.length
        for i, track in enumerate(midi_file.tracks):
            print("\n")
            print("TRACK\n")
            print(track)
            print("\n")
            print("NOTES\n")
            start_messages_list = []
            end_messages_list = []
            '''
            It is important to check for both velocity = 0 
            and type = 'note_off', because both are used as
            a mean to stop sounding a note.
            '''
            total_start_messages_time = 0
            total_end_messages_time = 0
            for msg in track:
                if msg.type == 'set_tempo':
                    self.tempo = msg.tempo
                if msg.type == 'note_on':
                    if msg.velocity != 0:
                        total_start_messages_time += msg.time
                        start_messages_list.append(msg)
                    else:
                        total_end_messages_time += msg.time
                        end_messages_list.append(msg)
                elif msg.type == 'note_off':
                    total_end_messages_time += msg.time
                    end_messages_list.append(msg)
            # print("Total start messages time in seconds: " + str(total_start_messages_time))
            # print("Total end messages time in seconds: " + str(total_end_messages_time))
            # print("Total messages time in seconds: " + str(total_start_messages_time + total_end_messages_time))
            # print("Total start messages time in ticks: " + str(second2tick(total_start_messages_time, midi_file.ticks_per_beat, self.tempo)))
            # print("Total end messages time in ticks: " + str(second2tick(total_end_messages_time, midi_file.ticks_per_beat, self.tempo)))
            total_delta_time = sum([abs(end.time - start.time) for start, end in zip(start_messages_list, end_messages_list)])
            # print("Total delta time in seconds: " + str(total_delta_time))
            # print('Track {}: {}'.format(i, track.name))
            # print("Number of start messages: " + str(len(start_messages_list)))
            # print("Number of end messages: " + str(len(end_messages_list)))
            # print("End messages: ")
            # print(*Counter(end.time for start, end in zip(start_messages_list, end_messages_list)))
            min_track_rhytm_val = min(filter(lambda x : x >0, Counter([end.time for end in end_messages_list]).keys()))
            if min_track_rhytm_val < self.minimum_rhytmic_value:
                 self.minimum_rhytmic_value = min_track_rhytm_val
            # for start, end in zip(start_messages_list, end_messages_list):
            #     print("Start message")
            #     print(start)
            #     print("End message")
            #     print(end)
            if len(end_messages_list) > 0:
                self.raw_tracks.append({'start':start_messages_list, 'end':end_messages_list})

        print("Minimum rhytmic value: " + str(self.minimum_rhytmic_value))
        self.track_count = len(midi_file.tracks)
        # quarter_note_count = int(midi_file.length / quarter_note_length)
        # print("Quarter note length: " + str(quarter_note_length))
        # print("Quarter note count: " + str(quarter_note_count))
        '''
        Calculation of the number of minimal notes present in the piece
        '''
        self.notes_quantity = int(float(self.total_time) * 1000 / float(self.minimum_rhytmic_value))
        quarter_note_length = second2tick(float(self.tempo) / 1000000.0, self.ticks_per_beat, self.tempo)
        self.rhytmic_values_duration = RhytmicValuesDuration(quarter_note_length * 4, quarter_note_length * 2,
        quarter_note_length, quarter_note_length/2, quarter_note_length/4, quarter_note_length/8, quarter_note_length/16)
        for track in self.raw_tracks:
            self.processed_tracks.append(self.process_track(track['start'], track['end']))




    def process_track(self, start_messages, end_messages):
        print("PROCESSING TRACK")
        processed_track = []
        chord = []
        for start, end in zip(start_messages, end_messages):
            to_append = None
            if end.time == self.rhytmic_values_duration.WHOLE - 1:
                to_append = RhytmicValues.WHOLE
            elif end.time == self.rhytmic_values_duration.HALF - 1:
                to_append = RhytmicValues.HALF
            elif end.time == self.rhytmic_values_duration.QUARTER - 1:
                to_append = RhytmicValues.QUARTER
            elif end.time == self.rhytmic_values_duration.EIGHT - 1:
                to_append = RhytmicValues.EIGHT
            elif end.time == self.rhytmic_values_duration.SIXTEEN - 1:
                to_append = RhytmicValues.SIXTEEN
            elif end.time == self.rhytmic_values_duration.THIRTY_TWO - 1:
                to_append = RhytmicValues.THIRTY_TWO
            elif end.time == self.rhytmic_values_duration.SIXTY_FOUR - 1:
                to_append = RhytmicValues.SIXTY_FOUR

            note = NoteWithDuration(Note(start.note % 12), duration=to_append)
            if len(chord) == 0 or start.time == 0:
                chord.append(note)
            elif len(chord) > 1:
                processed_track.append(ProcessedElement(is_chord=True, notes=chord))
                print("ADD CHORD")
                chord = []
            else:
                processed_track.append(ProcessedElement(is_chord=False, notes=[chord[0]]))
                processed_track.append(ProcessedElement(is_chord=False, notes=[note]))
                print("TO APPEND")
                print(to_append)
                print("CLEAR CHORD")
                print(*chord)
                chord = []

        if len(chord) == 1:
            processed_track.append(ProcessedElement(is_chord=False, notes=[chord[0]]))
        print("Processed track")
        print(*processed_track)
        print("\n\n\n")
        return processed_track


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

    def calculate_signature(self, window_start, window_end, mode):
        sig_util = SignatureOfFifthsUtility()
        notes_dict = sig_util.initialize_empty_notes_dict()
        print("Window start: " + str(window_start))
        print("Window end: " + str(window_end))
        print("Track")
        start_time_point = self.minimum_rhytmic_value * window_start
        end_time_point = self.minimum_rhytmic_value * window_end
        for track in self.tracks:
            if track.activated is True:
                if mode == SignatureModes.QUANTITY:
                    notes_dict += track.extract_note_messages_quantity(start_time_point, end_time_point)
                elif mode == SignatureModes.DURATION:
                    notes_dict += track.extract_note_messages_duration(start_time_point, end_time_point)
        signature = sig_util.calculate_signature_of_fifths(notes_dict)
        print("NOTES DICT: ")
        for x, y in notes_dict.items():
            print(x, y)
        print("SIGNATURE DICT: ")
        for x, y in signature.signature.items():
            print(x, y)
        print("\n")
        return signature
