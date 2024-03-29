
from model.definitions import Note, RhythmicValuesDuration, RawElement, ProcessedElement, NoteWithDuration, \
    RhythmicValues, Tempo, SampleMode, RhythmicValuesDurationWithStartTime
from mido import second2tick
from dataclasses import asdict

class Track:
    def __init__(self, processed_track, rhythmic_values=None, activated=False, number=0):
        self.processed_track = processed_track
        self.activated = activated
        self.number = number
        self.window_start = 0
        self.window_end = 0
        self.rhythmic_values = rhythmic_values

    def extract_note_messages_quantity(self, start_time_point, end_time_point, note_type):
        messages = self.get_messages_from_window(start_time_point, end_time_point, note_type)
        notes = {Note.C: 0, Note.C_SHARP: 0, Note.D: 0, Note.D_SHARP: 0, Note.E: 0, Note.F: 0, Note.F_SHARP: 0,
                 Note.G: 0, Note.G_SHARP: 0, Note.A: 0, Note.A_SHARP: 0, Note.B: 0}
        for note_with_duration in messages:
            if note_with_duration.note is not None:
                notes[note_with_duration.note] += 1
        return notes

    def extract_note_messages_duration(self, start_time_point, end_time_point, note_type):
        messages = self.get_messages_from_window(start_time_point, end_time_point, note_type)
        notes = {Note.C: 0, Note.C_SHARP: 0, Note.D: 0, Note.D_SHARP: 0, Note.E: 0, Note.F: 0, Note.F_SHARP: 0,
                 Note.G: 0, Note.G_SHARP: 0, Note.A: 0, Note.A_SHARP: 0, Note.B: 0}
        for msg in messages:
            if msg.note is not None:
                notes[msg.note] += msg.duration
        return notes

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

    def set_window(self, start, end):
        self.window_start = start
        self.window_end = end

    def get_messages_from_window(self, start_note, end_note, note_type):
        rhythm_val_iter = 0
        note_time = asdict(self.rhythmic_values[rhythm_val_iter].rhythmic_values_duration)[note_type]
        start_time = start_note * note_time
        end_time = end_note * note_time
        time_passed = 0
        track_iter = 0
        messages = []
        while time_passed < start_time and track_iter < len(self.processed_track):
            if rhythm_val_iter + 1 < len(self.rhythmic_values) and time_passed >= self.rhythmic_values[
                rhythm_val_iter + 1].start_time:
                rhythm_val_iter += 1
            time_passed += self.processed_track[track_iter].raw_duration
            track_iter += 1
        while time_passed < end_time and track_iter < len(self.processed_track):
            is_first_iteration = True
            for element in self.processed_track[track_iter].notes:
                note_time = 0
                for rhythmic_value in element.duration:
                    name = rhythmic_value.name
                    '''
                    A rounding for values with duration shorter than current tempo's sixty-four.
                    '''
                    if rhythmic_value.name == "LOWER_THAN_SIXTY_FOUR":
                        name = "SIXTY_FOUR"
                    if rhythm_val_iter + 1 < len(self.rhythmic_values) and time_passed >= self.rhythmic_values[rhythm_val_iter + 1].start_time:
                        rhythm_val_iter += 1
                    '''
                    This check is needed because when a chord is analysed, multiple notes are played continuously, and their
                    duration time should only be added once to the total duration time. Possible improvement: if the notes
                    in the self.processed_track[track_iter].notes have not equal duration, choose the longest/smallest/mean
                    duration. Now the algorithm adds the first encountered duration and adds it to the total passed time of the piece.
                    '''
                    if is_first_iteration:
                        time_passed += asdict(self.rhythmic_values[rhythm_val_iter].rhythmic_values_duration)[name]
                    note_time += asdict(self.rhythmic_values[rhythm_val_iter].rhythmic_values_duration)[name]
                    if note_time >= end_time:
                        break
                if not element.is_pause:
                    messages.append(NoteWithDuration(element.note, False, note_time))
                is_first_iteration = False
            track_iter += 1
        return messages

    '''
    Test scenarios:
    1. Test for tracks with chords.
    2. Test for tracks where too big note has been selected.
    '''
    def check_base_rhythmic_value_multiplicity(self, note_type):
        time_passed = 0
        rhytm_val_iter = 0
        processed_element_internal_index = 0
        notes_iter = 0
        note_time = asdict(self.rhythmic_values[rhytm_val_iter].rhythmic_values_duration)[note_type.name]
        actual_note_time = note_time
        time_passed = note_time
        time_to_full_note = 0
        #iterate over elements representing chords, pauses and single notes
        for track_element in self.processed_track:
            # #iterate over notes that make a chord, pause or single note
            note = track_element.notes[0]
            note_internal_index = 0
            #iterate over rhythmic values that make a single note
            while note_internal_index < len(note.duration) and \
                    note.duration[note_internal_index].name in asdict(self.rhythmic_values[rhytm_val_iter].rhythmic_values_duration).keys():
                # if there is a bigger note in track increment notes iterator and actual_note_time until actual_note_time is bigger than this note
                if actual_note_time < asdict(self.rhythmic_values[rhytm_val_iter].rhythmic_values_duration)[note.duration[note_internal_index].name]:
                    notes_iter += 1
                    time_passed += note_time
                    actual_note_time += note_time
                #if there is a smaller note in track, add its duration to actual_note_time so it can be increased to given note_type duration
                #and result in incrementing notes_iter
                elif actual_note_time == asdict(self.rhythmic_values[rhytm_val_iter].rhythmic_values_duration)[note.duration[note_internal_index].name]:
                    actual_note_time = note_time
                    notes_iter += 1
                    note_internal_index += 1
                elif actual_note_time > asdict(self.rhythmic_values[rhytm_val_iter].rhythmic_values_duration)[note.duration[note_internal_index].name]:
                    time_to_full_note += asdict(self.rhythmic_values[rhytm_val_iter].rhythmic_values_duration)[note.duration[note_internal_index].name]
                    note_internal_index += 1
                if time_to_full_note >= note_time:
                    notes_iter += 1
                    time_to_full_note = time_to_full_note - note_time # what to do with the remainder ?
                if rhytm_val_iter + 1 < len(self.rhythmic_values) and time_passed >= self.rhythmic_values[rhytm_val_iter].start_time:
                    rhytm_val_iter += 1
                    note_time = asdict(self.rhythmic_values[rhytm_val_iter].rhythmic_values_duration)[note_type.name]
        return notes_iter

class TrackManager:
    def __init__(self):
        self.raw_tracks = []
        self.processed_tracks = []
        self.track_count = 0
        self.notes_quantity = 0
        self.total_time = 0
        self.minimum_rhythmic_value = float('inf')
        self.tempos = []
        self.rhythmic_values_duration = RhythmicValuesDuration(2000000, 1000000, 500000, 250000, 125000, 62500, 31250)
        self.rhythmic_values_multiplicity = 0
        self.ticks_per_beat = 0

    def get_operable_range_of_all_tracks(self):
        lengths = []
        for track in self.processed_tracks:
            lengths.append(len(track.processed_track))
        return min(lengths)

    def activate_all_tracks(self):
        for track in self.processed_tracks:
            track.activate()

    def process_file(self, midi_file):
        self.ticks_per_beat = midi_file.ticks_per_beat
        self.total_time = midi_file.length
        for i, track in enumerate(midi_file.tracks):
            messages = []
            print("TRACK\n")
            print(track)
            '''
            It is important to check for both velocity = 0 
            and type = 'note_off', because both are used as
            a mean to stop sounding a note.
            '''
            start_notes = []
            end_notes = []
            pair_of_control_messages = []
            is_meta_track = True
            total_time_for_set_tempos = 0
            for msg in track:
                if msg.type == 'set_tempo':
                    total_time_for_set_tempos += msg.time
                    self.tempos.append(Tempo(tempo=msg.tempo, start_time=total_time_for_set_tempos))
                if not msg.is_meta:
                    is_meta_track = False
                    if msg.type == 'note_on' and msg.velocity != 0:
                        print(str(msg) + " NOTE " + Note(msg.note % 12).name)
                        if msg.time > 1:
                            messages.append(RawElement(is_chord=False, is_pause=True, start_notes=[msg], end_notes=None,
                                                       control=None, raw_duration=0))
                        start_notes.append(msg)
                    elif (msg.type == 'note_on' and msg.velocity == 0) or msg.type == 'note_off':
                        print(str(msg) + " NOTE " + Note(msg.note % 12).name)
                        end_notes.append(msg)
                        if len(start_notes) == len(end_notes):
                            raw_element = RawElement(False, False, None, None, None, 0)
                            raw_element.start_notes = start_notes
                            raw_element.end_notes = end_notes
                            if len(start_notes) > 1:
                                raw_element.is_chord = True
                            if len(pair_of_control_messages) == 2:
                                raw_element.control = pair_of_control_messages
                            raw_element.raw_duration = self.calculate_notes_raw_duration(raw_element)
                            messages.append(raw_element)
                            start_notes = []
                            end_notes = []
                            pair_of_control_messages = []
                    elif msg.type == 'control_change' and len(start_notes) != 0:
                        pair_of_control_messages.append(msg)
            if not is_meta_track and len(messages) > 0:
                self.raw_tracks.append(messages)
        self.track_count = len(self.raw_tracks)
        self.process_tracks()

    def process_tracks(self):
        '''
        Calculation of the number of minimal notes present in the piece
        '''
        track_iter = 0
        for raw_track in self.raw_tracks:
            track_iter += 1
            processed_track = []
            rhythmic_values_with_start_time = []
            total_time = 0
            tempos_index = 0
            actual_tempo = self.tempos[0].tempo
            self.calculate_rhythmic_values_duration(actual_tempo)
            rhythmic_values_with_start_time.append(
                RhythmicValuesDurationWithStartTime(start_time=self.tempos[tempos_index].start_time,
                                                   rhythmic_values_duration=self.rhythmic_values_duration))
            for raw_element in raw_track:
                total_time += raw_element.raw_duration
                if len(self.tempos) > tempos_index + 1 and self.tempos[tempos_index + 1].start_time <= total_time:
                    tempos_index += 1
                    actual_tempo = self.tempos[tempos_index].tempo
                    self.calculate_rhythmic_values_duration(actual_tempo)
                    rhythmic_values_with_start_time.append(RhythmicValuesDurationWithStartTime(start_time=self.tempos[tempos_index].start_time,
                                                                                             rhythmic_values_duration=self.rhythmic_values_duration))
                processed_track.append(self.process_raw_element(raw_element))
            self.processed_tracks.append(Track(processed_track=processed_track, number=track_iter, rhythmic_values=rhythmic_values_with_start_time))

    def calculate_rhythmic_values_duration(self, tempo):
        quarter_note_length = second2tick(float(tempo) / 1000000.0, self.ticks_per_beat, tempo)
        self.rhythmic_values_duration = RhythmicValuesDuration(quarter_note_length * 4, quarter_note_length * 2,
                                                             quarter_note_length, quarter_note_length / 2,
                                                             quarter_note_length / 4, quarter_note_length / 8,
                                                             quarter_note_length / 16)

    def calculate_notes_raw_duration(self, element):
        duration = 0
        if element.end_notes[0].time != 0:
            duration += element.end_notes[0].time
        if element.control is not None:
            duration += element.control[1].time
        return duration

    def process_raw_element(self, element):
        notes = []
        if element.is_pause:
            new_pause = NoteWithDuration(note=None, is_pause=True,
                                          duration=self.map_rhythmic_values(element.start_notes[0].time))
            notes.append(new_pause)
            return ProcessedElement(is_chord=False, notes=notes, raw_duration=element.start_notes[0].time)
        for end in element.end_notes:
            new_note = NoteWithDuration(note=Note(end.note % 12), is_pause=False, duration=self.map_rhythmic_values(end.time + 1))
            notes.append(new_note)

        return ProcessedElement(is_chord=(len(element.end_notes) != 1), notes=notes, raw_duration=element.raw_duration)

    def map_rhythmic_values(self, time):
        to_return = []
        time = time + 1
        while time > 0:
            if time >= self.rhythmic_values_duration.WHOLE:
                to_return.extend([RhythmicValues.WHOLE] * int(time / self.rhythmic_values_duration.WHOLE))
                time %= self.rhythmic_values_duration.WHOLE
            elif time >= self.rhythmic_values_duration.HALF:
                to_return.extend([RhythmicValues.HALF] * int(time / self.rhythmic_values_duration.HALF))
                time %= self.rhythmic_values_duration.HALF
            elif time >= self.rhythmic_values_duration.QUARTER:
                to_return.extend([RhythmicValues.QUARTER] * int(time / self.rhythmic_values_duration.QUARTER))
                time %= self.rhythmic_values_duration.QUARTER
            elif time >= self.rhythmic_values_duration.EIGHT:
                to_return.extend([RhythmicValues.EIGHT] * int(time / self.rhythmic_values_duration.EIGHT))
                time %= self.rhythmic_values_duration.EIGHT
            elif time >= self.rhythmic_values_duration.SIXTEEN:
                to_return.extend([RhythmicValues.SIXTEEN] * int(time / self.rhythmic_values_duration.SIXTEEN))
                time %= self.rhythmic_values_duration.SIXTEEN
            elif time >= self.rhythmic_values_duration.THIRTY_TWO:
                to_return.extend([RhythmicValues.THIRTY_TWO] * int(time / self.rhythmic_values_duration.THIRTY_TWO))
                time %= self.rhythmic_values_duration.THIRTY_TWO
            elif time >= self.rhythmic_values_duration.SIXTY_FOUR:
                to_return.extend([RhythmicValues.SIXTY_FOUR] * int(time / self.rhythmic_values_duration.SIXTY_FOUR))
                time %= self.rhythmic_values_duration.SIXTY_FOUR
            else:
                to_return.append(RhythmicValues.LOWER_THAN_SIXTY_FOUR)
                time = 0
        return to_return

    def activate_track(self, track_number):
        if track_number < self.track_count:
            self.processed_tracks[track_number].activate()

    def deactivate_track(self, track_number):
        if track_number < self.track_count:
            self.processed_tracks[track_number].deactivate()

    def handle_selection(self, track_number):
        if self.processed_tracks[track_number].activated is True:
            self.processed_tracks[track_number].deactivate()
        else:
            self.processed_tracks[track_number].activate()

    def is_track_selected(self, track_number):
        return self.processed_tracks[track_number].activated

    def get_selected_tracks_numbers(self):
        return [track.number for track in self.processed_tracks if track.activated]

    def calculate_sample_vector(self, window_start, window_end, mode, base_rhythmic_value):
        notes_dict = {Note.C: 0, Note.C_SHARP: 0, Note.D: 0, Note.D_SHARP: 0, Note.E: 0, Note.F: 0, Note.F_SHARP: 0,
                      Note.G: 0, Note.G_SHARP: 0, Note.A: 0, Note.A_SHARP: 0, Note.B: 0}
        for track in self.processed_tracks:
            if track.activated is True:
                new_notes_dict = {}
                if mode == SampleMode.QUANTITY:
                    new_notes_dict = track.extract_note_messages_quantity(window_start, window_end, base_rhythmic_value)
                elif mode == SampleMode.DURATION:
                    new_notes_dict = track.extract_note_messages_duration(window_start, window_end, base_rhythmic_value)

                for key in notes_dict.keys():
                    notes_dict[key] += new_notes_dict[key]
                #notes_dict = {i: notes_dict.get(i, 0) + new_notes_dict.get(i, 0) for i in set(notes_dict).union(new_notes_dict)}
        return notes_dict

    def calculate_base_rhythmic_value_multiplicity(self, note_type):
        return self.processed_tracks[0].check_base_rhythmic_value_multiplicity(note_type)
