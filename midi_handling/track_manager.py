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
    LOWER_THAN_SIXTY_FOUR=65

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
class RawElement:
    is_chord: bool
    is_pause: bool
    start_notes: []
    end_notes: []
    control: []

'''
A note or group of notes that have the same duration
'''
@dataclass
class ProcessedElement:
    is_chord: bool # if the element is a chord, i.e. if more than one note is played simultaneously
    notes: [] # total duration represented as collection of notes
    raw_duration: int   # total duration represented as integer

@dataclass
class NoteWithDuration:
    note: Note
    is_pause: bool
    duration: RhytmicValues

@dataclass
class ProcessedTrack:
    elements: []


class Track:
    def __init__(self, processed_track, rhytmic_values=None, activated=False, number=0):
        self.processed_track = processed_track
        self.activated = activated
        self.number = number
        self.window_start = 0
        self.window_end = 0
        self.rhytmic_values = rhytmic_values

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
        notes = {Note.C: 0, Note.C_SHARP: 0, Note.D: 0, Note.D_SHARP: 0, Note.E: 0, Note.F: 0, Note.F_SHARP: 0,
                 Note.G: 0, Note.G_SHARP: 0, Note.A: 0, Note.A_SHARP: 0, Note.B: 0}
        print("Notes window")
        print(messages)
        for msg in messages:
            for note_with_duration in msg.notes:
                if note_with_duration.note != None:
                    notes[note_with_duration.note] += msg.raw_duration

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

    def get_messages_from_window(self, start_note, end_note):
        # start = start_note * self.rhytmic_values.SIXTY_FOUR
        # end = end_note * self.rhytmic_values.SIXTY_FOUR
        start, start_remainder = self.iterate_to_value(start_note)
        end, end_remainder = self.iterate_to_value(end_note)
        messages = self.processed_track[start:end]
        # messages = self.add_remainder(messages, start, start_remainder)
        # messages = self.add_remainder(messages, end, end_remainder)
        return messages

    def add_remainder(self, messages, index, remainder):
        if(remainder > 0):
            if not messages[index].is_chord:
                messages[index] = ProcessedElement(false,
                                               NoteWithDuration(messages[index].notes[0].note, messages[index].notes[0].duration - remainder))
            else:
                messages[index].notes = [NoteWithDuration(note.note, note.duration - remainder) for note in messages[index].notes]
        return messages

    def iterate_to_value(self, target_offset):
        current_offset = 0
        for index in range(0, len(self.processed_track)):
            progress_offset = current_offset + self.processed_track[index].raw_duration
            if progress_offset < target_offset:
                current_offset = progress_offset
            elif progress_offset == target_offset:
                return index + 1, 0 #value is obtained at index one before desired start index
            else:
                return index + 1, progress_offset - target_offset
        return 0, 0


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
            messages = []
            '''
            It is important to check for both velocity = 0 
            and type = 'note_off', because both are used as
            a mean to stop sounding a note.
            '''
            start_notes = []
            end_notes = []
            pair_of_control_messages = []
            for msg in track:
                if msg.type == 'set_tempo':
                    self.tempo = msg.tempo
                if msg.type == 'note_on' and msg.velocity != 0:
                    if msg.time > 1:
                        messages.append(RawElement(is_chord=False, is_pause=True, start_notes=[msg], end_notes=None, control=None))
                    start_notes.append(msg)
                elif (msg.type == 'note_on' and msg.velocity == 0) or msg.type == 'note_off':
                    end_notes.append(msg)
                    if len(start_notes) == len(end_notes):
                        raw_element = RawElement(False, False, None, None, None)
                        raw_element.start_notes = start_notes
                        raw_element.end_notes = end_notes
                        if len(start_notes) > 0:
                            raw_element.is_chord == True
                        if len(pair_of_control_messages) == 2:
                            raw_element.control = pair_of_control_messages
                        messages.append(raw_element)
                        start_notes = []
                        end_notes = []
                        pair_of_control_messages = []
                elif msg.type == 'control_change' and len(start_notes) != 0:
                    pair_of_control_messages.append(msg)

            # print("Total start messages time in seconds: " + str(total_start_messages_time))
            # print("Total end messages time in seconds: " + str(total_end_messages_time))
            # print("Total messages time in seconds: " + str(total_start_messages_time + total_end_messages_time))
            # print("Total start messages time in ticks: " + str(second2tick(total_start_messages_time, midi_file.ticks_per_beat, self.tempo)))
            # print("Total end messages time in ticks: " + str(second2tick(total_end_messages_time, midi_file.ticks_per_beat, self.tempo)))
            # total_delta_time = sum([abs(end.time - start.time) for start, end in zip(start_messages_list, end_messages_list)])
            # print("Total delta time in seconds: " + str(total_delta_time))
            # print('Track {}: {}'.format(i, track.name))
            # print("Number of start messages: " + str(len(start_messages_list)))
            # print("Number of end messages: " + str(len(end_messages_list)))
            # print("End messages: ")
            # print(*Counter(end.time for start, end in zip(start_messages_list, end_messages_list)))
            if len(messages) > 0:
                min_track_rhytm_val = float('inf')
                for element in messages:
                    if not element.is_pause:
                        time = max([note.time for note in element.end_notes])
                    if time < min_track_rhytm_val:
                        min_track_rhytm_val = time
                #min_track_rhytm_val = min(filter(lambda x : x >0, Counter([max([note.time for note in element.notes]) for element in messages]).keys()))
                if min_track_rhytm_val < self.minimum_rhytmic_value:
                     self.minimum_rhytmic_value = min_track_rhytm_val + 1 # add one because in the messages values are one smaller
                self.raw_tracks.append(messages)
            # for start, end in zip(start_messages_list, end_messages_list):
            #     print("Start message")
            #     print(start)
            #     print("End message")
            #     print(end)
        print("Minimum rhytmic value: " + str(self.minimum_rhytmic_value))
        self.track_count = len(midi_file.tracks)
        # quarter_note_count = int(midi_file.length / quarter_note_length)
        # print("Quarter note length: " + str(quarter_note_length))
        # print("Quarter note count: " + str(quarter_note_count))
        self.process_tracks()
        print("")

    def process_tracks(self):
        '''
        Calculation of the number of minimal notes present in the piece
        '''
        #self.notes_quantity = int(float(self.total_time) * 1000 / float(self.minimum_rhytmic_value))
        quarter_note_length = second2tick(float(self.tempo) / 1000000.0, self.ticks_per_beat, self.tempo)
        self.rhytmic_values_duration = RhytmicValuesDuration(quarter_note_length * 4, quarter_note_length * 2,
        quarter_note_length, quarter_note_length/2, quarter_note_length/4, quarter_note_length/8, quarter_note_length/16)
        for raw_track in self.raw_tracks:
            processed_track = []
            for raw_element in raw_track:
                processed_track.append(self.process_raw_element(raw_element))
            self.processed_tracks.append(Track(processed_track=processed_track, rhytmic_values=self.rhytmic_values_duration))

    def map_rhytmic_values(self, time):
        to_return = []
        time = time + 1
        while time > 0:
            if time >= self.rhytmic_values_duration.WHOLE:
                to_return.extend([RhytmicValues.WHOLE] * int(time / self.rhytmic_values_duration.WHOLE))
                time %= self.rhytmic_values_duration.WHOLE
            elif time >= self.rhytmic_values_duration.HALF:
                to_return.extend([RhytmicValues.HALF] * int(time / self.rhytmic_values_duration.HALF))
                time %= self.rhytmic_values_duration.HALF
            elif time >= self.rhytmic_values_duration.QUARTER:
                to_return.extend([RhytmicValues.QUARTER] * int(time / self.rhytmic_values_duration.QUARTER))
                time %= self.rhytmic_values_duration.QUARTER
            elif time >= self.rhytmic_values_duration.EIGHT:
                to_return.extend([RhytmicValues.EIGHT] * int(time / self.rhytmic_values_duration.EIGHT))
                time %= self.rhytmic_values_duration.EIGHT
            elif time >= self.rhytmic_values_duration.SIXTEEN:
                to_return.extend([RhytmicValues.SIXTEEN] * int(time / self.rhytmic_values_duration.SIXTEEN))
                time %= self.rhytmic_values_duration.SIXTEEN
            elif time >= self.rhytmic_values_duration.THIRTY_TWO:
                to_return.extend([RhytmicValues.THIRTY_TWO] * int(time / self.rhytmic_values_duration.THIRTY_TWO))
                time %= self.rhytmic_values_duration.THIRTY_TWO
            elif time >= self.rhytmic_values_duration.SIXTY_FOUR:
                to_return.extend([RhytmicValues.SIXTY_FOUR] * int(time / self.rhytmic_values_duration.SIXTY_FOUR))
                time %= self.rhytmic_values_duration.SIXTY_FOUR
            else:
                to_return.append(RhytmicValues.LOWER_THAN_SIXTY_FOUR)
                time = 0
        return to_return

    def process_raw_element(self, element):
        notes = []
        duration = 0
        if element.is_pause:
            notes.append(NoteWithDuration(note=None, is_pause=True, duration=self.map_rhytmic_values(element.start_notes[0].time)))
            return ProcessedElement(is_chord=False, notes=notes, raw_duration=element.start_notes[0].time)

        for end in element.end_notes:
            if end.time != 0:
                duration += end.time
                if element.control != None:
                    duration += element.control[1].time

        for end in element.end_notes:
            notes.append(NoteWithDuration(note=Note(end.note % 12), is_pause=False, duration=self.map_rhytmic_values(duration)))

        return ProcessedElement(is_chord=(len(element.end_notes) != 1), notes=notes, raw_duration=duration + 1)

    def activate_track(self, track_number):
        if track_number < self.track_count:
            self.processed_tracks[track_number].activate()

    def deactivate_track(self, track_number):
        if track_number < self.track_count:
            self.processed_tracks[track_number].deactivate()

    def handle_selection(self, track_number):
        if (self.processed_tracks[track_number].activated is True):
            self.processed_tracks[track_number].deactivate()
        else:
            self.processed_tracks[track_number].activate()

    def is_track_selected(self, track_number):
        return self.processed_tracks[track_number].activated

    def calculate_signature(self, window_start, window_end, mode):
        sig_util = SignatureOfFifthsUtility()
        notes_dict = sig_util.initialize_empty_notes_dict()
        print("Window start: " + str(window_start))
        print("Window end: " + str(window_end))
        print("Track")
        start_time_point = self.rhytmic_values_duration.EIGHT * (window_start - 1)#input values like 1 - 3, translate to values like 0 - 2 (proper array indexing)
        end_time_point = self.rhytmic_values_duration.EIGHT * (window_end)
        for track in self.processed_tracks:
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
