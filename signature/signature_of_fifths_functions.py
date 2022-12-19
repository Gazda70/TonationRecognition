from enum import Enum
from collections import Counter
from dataclasses import dataclass, asdict
from mido import MidiFile
import numpy as np
import math

from utils.vector_operations import add_vector_list

NOTE_VECTOR_MAX_LENGTH = 2

"""
    It has to be in such order because of the numeration of notes used by MIDI standard.
"""
class Note(Enum):
    C, C_SHARP, D, D_SHARP, E, F, F_SHARP, G, G_SHARP, A, A_SHARP, B = range(12)

class NoteVectorDirection(Enum):
    C_DIR, G_DIR, D_DIR, A_DIR, E_DIR, B_DIR , F_SHARP_DIR, C_SHARP_DIR, G_SHARP_DIR, D_SHARP_DIR , A_SHARP_DIR, F_DIR = \
        range(0, 360, 30)


# (Y; Z) ∈ {(C, F♯); (F, B); (B, E); (E, A); (A, D); (D, G); (F♯, C); (B, F); (E, B); (A, E); (D, A); (G, D)}
# WHAT ABOUT THE TONATIONS THAT LIE EXACTLY ON THE AXIS ? - THEY ARE NOT COUNTED
@dataclass
class DirectedAxis:
    AXIS_C_Fsharp: dict
    AXIS_F_B: dict
    AXIS_Asharp_E: dict
    AXIS_Dsharp_A: dict
    AXIS_Gsharp_D: dict
    AXIS_Csharp_G: dict
    AXIS_Fsharp_C: dict
    AXIS_B_F: dict
    AXIS_E_Asharp: dict
    AXIS_A_Dsharp: dict
    AXIS_D_Gsharp: dict
    AXIS_G_Csharp: dict


def create_directed_axis_object():
    return {
        "AXIS_C_Fsharp":{"positive": [(Note.G, 0), (Note.D, 0), (Note.A, 0), (Note.E, 0), (Note.B, 0)],
                       "negative": [(Note.F, 0), (Note.A_SHARP, 0), (Note.D_SHARP, 0), (Note.G_SHARP, 0),
                                    (Note.C_SHARP, 0), (Note.F_SHARP, 0)],
                         "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.F_SHARP_DIR.value))},
        "AXIS_F_B" : {"positive": [(Note.C, 0), (Note.G, 0), (Note.D, 0), (Note.A, 0),
                                   (Note.E, 0)],
                  "negative": [(Note.A_SHARP, 0), (Note.D_SHARP, 0), (Note.G_SHARP, 0), (Note.C_SHARP, 0),
                               (Note.F_SHARP, 0)],
                      "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.B_DIR.value))},
        "AXIS_Asharp_E" : {"positive": [(Note.F,0), (Note.C, 0), (Note.G, 0), (Note.D, 0), (Note.A, 0)],
                       "negative": [(Note.D_SHARP, 0), (Note.G_SHARP, 0), (Note.C_SHARP, 0),
                                    (Note.F_SHARP, 0), (Note.B, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.E_DIR.value))},
        "AXIS_Dsharp_A" : {"positive": [(Note.A_SHARP, 0), (Note.F, 0), (Note.C, 0), (Note.G, 0), (Note.D, 0)],
                       "negative": [(Note.G_SHARP, 0), (Note.C_SHARP, 0),
                                    (Note.F_SHARP, 0), (Note.B, 0), (Note.E, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.A_DIR.value))},
        "AXIS_Gsharp_D" : {"positive": [(Note.G_SHARP, 0), (Note.D_SHARP, 0), (Note.A_SHARP, 0), (Note.F, 0),
                                        (Note.C, 0), (Note.G, 0)],
                       "negative": [(Note.C_SHARP, 0), (Note.F_SHARP, 0),
                                    (Note.B, 0), (Note.E, 0), (Note.A, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.D_DIR.value))},
        "AXIS_Csharp_G" : {"positive": [(Note.G_SHARP, 0), (Note.D_SHARP, 0), (Note.A_SHARP, 0),
                                        (Note.F, 0), (Note.C, 0)],
                       "negative": [(Note.F_SHARP, 0), (Note.B, 0),
                                    (Note.E, 0), (Note.A, 0), (Note.D, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.G_DIR.value))},
        "AXIS_Fsharp_C" : {"positive": [(Note.F, 0), (Note.A_SHARP, 0), (Note.D_SHARP, 0), (Note.G_SHARP, 0),
                                        (Note.C_SHARP, 0), (Note.F_SHARP, 0)],
                       "negative": [(Note.G, 0), (Note.D, 0), (Note.A, 0), (Note.E, 0), (Note.B, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.C_DIR.value))},
        "AXIS_B_F" : {"positive": [(Note.A_SHARP, 0), (Note.D_SHARP, 0), (Note.G_SHARP, 0), (Note.C_SHARP, 0),
                                   (Note.F_SHARP, 0)],
                  "negative": [(Note.C, 0), (Note.G, 0), (Note.D, 0), (Note.A, 0),
                               (Note.E, 0)],
                      "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.F_DIR.value))},
        "AXIS_E_Asharp" : {"positive": [(Note.D_SHARP, 0), (Note.G_SHARP, 0), (Note.C_SHARP, 0),
                                        (Note.F_SHARP, 0), (Note.B, 0)],
                       "negative": [(Note.F, 0), (Note.C, 0), (Note.G, 0), (Note.D, 0), (Note.A, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.A_SHARP_DIR.value))},
        "AXIS_A_Dsharp" : {"positive": [(Note.G_SHARP, 0), (Note.C_SHARP, 0),
                                        (Note.F_SHARP, 0), (Note.B, 0), (Note.E, 0)],
                       "negative": [(Note.A_SHARP, 0), (Note.F, 0), (Note.C, 0), (Note.G, 0), (Note.D, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.D_SHARP_DIR.value))},
        "AXIS_D_Gsharp" : {"positive": [(Note.C_SHARP, 0), (Note.F_SHARP, 0),
                                        (Note.B, 0), (Note.E, 0), (Note.A, 0)],
                       "negative": [(Note.G_SHARP, 0), (Note.D_SHARP, 0), (Note.A_SHARP, 0), (Note.F, 0),
                                    (Note.C, 0), (Note.G, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.G_SHARP_DIR.value))},
        "AXIS_G_Csharp" : {"positive": [(Note.F_SHARP, 0), (Note.B, 0),
                                        (Note.E, 0), (Note.A, 0), (Note.D, 0)],
                       "negative": [(Note.G_SHARP, 0), (Note.D_SHARP, 0), (Note.A_SHARP, 0),
                                    (Note.F, 0), (Note.C, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.C_SHARP_DIR.value))}
    }


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

        self.cvsf = None
        self.mdasf = None
        self.mode_angle = 0.0


class DirectedAxisCreator:
    def determine_from_signature(self, signature: SignatureOfFifths):
        directed_axis_collection = create_directed_axis_object()
        # print("directed_axis_collection")
        # print(directed_axis_collection)
        # print("signature.signature.keys()")
        # print(set(signature.signature.keys()))
        max_difference = -math.inf
        best_dir_ax = None
        for dir_ax in directed_axis_collection.keys():
            # print("ANOTHER AXIS")
            # print(dir_ax)
            # print(type(dir_ax))
            # print([element[0] for element in directed_axis_collection[dir_ax]["positive"]])
            # print([type(element[0]) for element in directed_axis_collection[dir_ax]["positive"]])
            positive_notes = set(signature.signature.keys()).intersection(
                set([element[0] for element in directed_axis_collection[dir_ax]["positive"]]))
            # print("positive_notes")
            # print(positive_notes)
            # print(type(positive_notes))
            positive_notes_sum = sum([signature.signature[positive_note].length for positive_note in positive_notes])

            negative_notes = set(signature.signature.keys()).intersection(
                set([element[0] for element in directed_axis_collection[dir_ax]["negative"]]))
            # print("negative_notes")
            # print(negative_notes)
            negative_notes_sum = sum([signature.signature[negative_note].length for negative_note in negative_notes])
            difference = positive_notes_sum - negative_notes_sum
            if difference > max_difference:
                max_difference = difference
                best_dir_ax = dir_ax
        print("Best axis")
        print(best_dir_ax)
        print("Max difference")
        print(max_difference)
        return directed_axis_collection[best_dir_ax]['note_vector']

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
            if msg.is_cc():
                print("CONTROL MESSAGE")
                print(msg)
            if msg.type == 'note_on':
                notes[Note(msg.note % 12)] += 1
                msg_types.append(msg.type)
        # print("MESSAGE TYPES: " + str(Counter(msg_types).keys()))
        # print("MESSAGE TYPES OCCURRENCE FREQUENCY: " + str(Counter(msg_types).values()))
        return notes

    def calculate_signature_of_fifths(self, notes) -> SignatureOfFifths:
        signature = SignatureOfFifths()
        for name, value in zip(notes.keys(), notes.values()):
            signature.signature[Note(name)].length = value / max(notes.values()) if max(notes.values()) != 0 else 0
        return signature

    def calculate_cvsf(self, signature: SignatureOfFifths) -> NoteVector:
        cvsf_vector = add_vector_list(
            list((note_vector.length, note_vector.direction) for note_vector in signature.signature.values()))
        cvsf = NoteVector(cvsf_vector[0], cvsf_vector[1])
        signature.cvsf = cvsf

    def calculate_mdasf(self, signature: SignatureOfFifths):
        creator = DirectedAxisCreator()
        mdasf = creator.determine_from_signature(signature)
        signature.mdasf = mdasf

    def calculate_mode_angle(self, signature: SignatureOfFifths):
        angle_one = signature.mdasf.direction + 90.0
        mode_angle = signature.cvsf.direction - angle_one
        print("mode_angle")
        print(mode_angle)
        signature.mode_angle = mode_angle