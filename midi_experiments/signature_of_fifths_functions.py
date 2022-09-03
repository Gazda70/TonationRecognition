from enum import Enum
from collections import Counter
from mido import MidiFile


class Note(Enum):
    C, C_SHARP, D, D_SHARP, E, F, F_SHARP, G, G_SHARP, A, A_SHARP, B = range(12)


class SignatureOfFifthsUtility:
    '''
        The function now counts the pitches frequency on the basis of the number of track's messages that
        have certain pitch's code - the more messages the more the note.
    '''
    def count_notes_in_track(self, track) -> {}:
        msg_types = []
        notes = {Note.C: 0, Note.C_SHARP: 0, Note.D: 0, Note.D_SHARP: 0, Note.E: 0, Note.F: 0, Note.F_SHARP: 0,
                 Note.G: 0, Note.G_SHARP: 0, Note.A: 0, Note.A_SHARP: 0, Note.B: 0}
        for msg in track:
            if msg.type == 'note_on':
                notes[Note(msg.note % 12)] += 1
                msg_types.append(msg.type)
        print("MESSAGE TYPES: " + str(Counter(msg_types).keys()))
        print("MESSAGE TYPES OCCURRENCE FREQUENCY: " + str(Counter(msg_types).values()))
        return notes
