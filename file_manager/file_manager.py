from mido import MidiFile
from file_manager.track_manager import TrackManager


class MidiReader:

    def read_file(self, midi_path):
        self.midi_file = MidiFile(midi_path, clip=True)
        track_manager = TrackManager()
        track_manager.process_file(self.midi_file)

        return track_manager




