from enum import Enum
from collections import Counter
from dataclasses import dataclass
from mido import MidiFile
import numpy as np

from utils.vector_operations import add_vector_list

"""
    It has to be in such order because of the numeration of notes used by MIDI standard.
"""


class Note(Enum):
    C, C_SHARP, D, D_SHARP, E, F, F_SHARP, G, G_SHARP, A, A_SHARP, B = range(12)


class NoteVectorDirection(Enum):
    A_DIR, D_DIR, G_DIR, C_DIR, F_DIR, A_SHARP_DIR, D_SHARP_DIR, G_SHARP_DIR, C_SHARP_DIR, F_SHARP_DIR, B_DIR, E_DIR = \
        range(0, 360, 30)


'''
for data in NoteVectorDirection:
    print('{:15} = {}'.format(data.name, data.value))
'''


@dataclass
class NoteVector:
    length: float
    direction: float


@dataclass
class SignatureOfFifths:
    def __init__(self):
        self.signature = {Note.A: NoteVector(0, NoteVectorDirection.A_DIR.value),
                          Note.D: NoteVector(0, NoteVectorDirection.D_DIR.value),
                          Note.G: NoteVector(0, NoteVectorDirection.G_DIR.value),
                          Note.C: NoteVector(0, NoteVectorDirection.C_DIR.value),
                          Note.F: NoteVector(0, NoteVectorDirection.F_DIR.value),
                          Note.C_SHARP: NoteVector(0, NoteVectorDirection.C_SHARP_DIR.value),
                          Note.D_SHARP: NoteVector(0, NoteVectorDirection.D_SHARP_DIR.value),
                          Note.E: NoteVector(0, NoteVectorDirection.E_DIR.value),
                          Note.F_SHARP: NoteVector(0, NoteVectorDirection.F_SHARP_DIR.value),
                          Note.G_SHARP: NoteVector(0, NoteVectorDirection.G_SHARP_DIR.value),
                          Note.A_SHARP: NoteVector(0, NoteVectorDirection.A_SHARP_DIR.value),
                          Note.B: NoteVector(0, NoteVectorDirection.B_DIR.value)}


class SignatureOfFifthsUtility:
    """
        The function now counts the pitches frequency on the basis of the number of track's messages that
        have certain pitch's code - the more messages the more the note.
    """

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

    def calculate_signature_of_fifths(self, notes) -> SignatureOfFifths:
        signature = SignatureOfFifths()
        for name, value in zip(notes.keys(), notes.values()):
            signature.signature[Note(name)].length = value / sum(notes.values()) if sum(notes.values()) != 0 else 0
        return signature

    def calculate_cvsf(self, signature:SignatureOfFifths) -> NoteVector:
        cvsf_vector = add_vector_list(list((note_vector.length, note_vector.direction)for note_vector in signature.signature.values()))
        return NoteVector(cvsf_vector[0], cvsf_vector[1])
