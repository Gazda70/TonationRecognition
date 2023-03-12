from signature.signature_of_fifths_functions import SignatureOfFifthsUtility

class Track:
    def __init__(self, track, activated=False, number=0):
        self.track = track
        self.activated = activated
        self.number = number

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

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
        if(self.tracks[track_number].activated is True):
            self.tracks[track_number].deactivate()
        else:
            self.tracks[track_number].activate()

    def is_track_selected(self, track_number):
        return self.tracks[track_number].activated



    def calculate_signature(self, sample):
        sig_util = SignatureOfFifthsUtility()
        notes_dict = sig_util.count_notes_in_track(track)
        signature = sig_util.calculate_signature_of_fifths(notes_dict)

        print("NOTES DICT: ")
        for x, y in notes_dict.items():
            print(x, y)
        print("SIGNATURE DICT: ")
        for x, y in signature.signature.items():
            print(x, y)
        print("\n")
        return signature