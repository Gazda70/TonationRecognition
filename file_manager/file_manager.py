from dataclasses import dataclass

from mido import MidiFile
from file_manager.track_manager import TrackManager

@dataclass
class FileInfo:
    file:MidiFile
    track_manager:TrackManager
    is_selected:bool
    file_number:int
class MidiReader:

    def read_file(self, midi_path):
        new_file = MidiFile(midi_path, clip=True)
        track_manager = TrackManager()
        track_manager.process_file(new_file)

        return new_file, track_manager
