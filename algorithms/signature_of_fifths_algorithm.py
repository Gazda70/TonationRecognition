from enum import Enum
from dataclasses import dataclass
import math
from collections import Counter
from utils.vector_operations import add_vector_list
from model.definitions import NOTE_VECTOR_MAX_LENGTH, SignatureOfFifths, Tonation, Note, NoteVector, NoteVectorDirection, Mode

def create_directed_axis_object():
    return {
        "AXIS_C_Fsharp":{"positive": [(Note.G, 0), (Note.D, 0), (Note.A, 0), (Note.E, 0), (Note.B, 0)],
                       "negative": [(Note.F, 0), (Note.A_SHARP, 0), (Note.D_SHARP, 0), (Note.G_SHARP, 0),
                                    (Note.C_SHARP, 0), (Note.F_SHARP, 0)],
                         "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.F_SHARP.value))},
        "AXIS_F_B" : {"positive": [(Note.C, 0), (Note.G, 0), (Note.D, 0), (Note.A, 0),
                                   (Note.E, 0)],
                  "negative": [(Note.A_SHARP, 0), (Note.D_SHARP, 0), (Note.G_SHARP, 0), (Note.C_SHARP, 0),
                               (Note.F_SHARP, 0)],
                      "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.B.value))},
        "AXIS_Asharp_E" : {"positive": [(Note.F,0), (Note.C, 0), (Note.G, 0), (Note.D, 0), (Note.A, 0)],
                       "negative": [(Note.D_SHARP, 0), (Note.G_SHARP, 0), (Note.C_SHARP, 0),
                                    (Note.F_SHARP, 0), (Note.B, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.E.value))},
        "AXIS_Dsharp_A" : {"positive": [(Note.A_SHARP, 0), (Note.F, 0), (Note.C, 0), (Note.G, 0), (Note.D, 0)],
                       "negative": [(Note.G_SHARP, 0), (Note.C_SHARP, 0),
                                    (Note.F_SHARP, 0), (Note.B, 0), (Note.E, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.A.value))},
        "AXIS_Gsharp_D" : {"positive": [(Note.G_SHARP, 0), (Note.D_SHARP, 0), (Note.A_SHARP, 0), (Note.F, 0),
                                        (Note.C, 0), (Note.G, 0)],
                       "negative": [(Note.C_SHARP, 0), (Note.F_SHARP, 0),
                                    (Note.B, 0), (Note.E, 0), (Note.A, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.D.value))},
        "AXIS_Csharp_G" : {"positive": [(Note.G_SHARP, 0), (Note.D_SHARP, 0), (Note.A_SHARP, 0),
                                        (Note.F, 0), (Note.C, 0)],
                       "negative": [(Note.F_SHARP, 0), (Note.B, 0),
                                    (Note.E, 0), (Note.A, 0), (Note.D, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.G.value))},
        "AXIS_Fsharp_C" : {"positive": [(Note.F, 0), (Note.A_SHARP, 0), (Note.D_SHARP, 0), (Note.G_SHARP, 0),
                                        (Note.C_SHARP, 0), (Note.F_SHARP, 0)],
                       "negative": [(Note.G, 0), (Note.D, 0), (Note.A, 0), (Note.E, 0), (Note.B, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.C.value))},
        "AXIS_B_F" : {"positive": [(Note.A_SHARP, 0), (Note.D_SHARP, 0), (Note.G_SHARP, 0), (Note.C_SHARP, 0),
                                   (Note.F_SHARP, 0)],
                  "negative": [(Note.C, 0), (Note.G, 0), (Note.D, 0), (Note.A, 0),
                               (Note.E, 0)],
                      "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.F.value))},
        "AXIS_E_Asharp" : {"positive": [(Note.D_SHARP, 0), (Note.G_SHARP, 0), (Note.C_SHARP, 0),
                                        (Note.F_SHARP, 0), (Note.B, 0)],
                       "negative": [(Note.F, 0), (Note.C, 0), (Note.G, 0), (Note.D, 0), (Note.A, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.A_SHARP.value))},
        "AXIS_A_Dsharp" : {"positive": [(Note.G_SHARP, 0), (Note.C_SHARP, 0),
                                        (Note.F_SHARP, 0), (Note.B, 0), (Note.E, 0)],
                       "negative": [(Note.A_SHARP, 0), (Note.F, 0), (Note.C, 0), (Note.G, 0), (Note.D, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.D_SHARP.value))},
        "AXIS_D_Gsharp" : {"positive": [(Note.C_SHARP, 0), (Note.F_SHARP, 0),
                                        (Note.B, 0), (Note.E, 0), (Note.A, 0)],
                       "negative": [(Note.G_SHARP, 0), (Note.D_SHARP, 0), (Note.A_SHARP, 0), (Note.F, 0),
                                    (Note.C, 0), (Note.G, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.G_SHARP.value))},
        "AXIS_G_Csharp" : {"positive": [(Note.F_SHARP, 0), (Note.B, 0),
                                        (Note.E, 0), (Note.A, 0), (Note.D, 0)],
                       "negative": [(Note.G_SHARP, 0), (Note.D_SHARP, 0), (Note.A_SHARP, 0),
                                    (Note.F, 0), (Note.C, 0)],
                           "note_vector":NoteVector(NOTE_VECTOR_MAX_LENGTH, float(NoteVectorDirection.C_SHARP.value))}
    }

class DirectedAxisCreator:
    def determine_from_signature(self, signature: SignatureOfFifths):
        directed_axis_collection = create_directed_axis_object()
        # print("directed_axis_collection")
        # print(directed_axis_collection)
        # print("algorithms.algorithms.keys()")
        # print(set(algorithms.algorithms.keys()))
        max_difference = -math.inf
        best_ax = None
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
                best_ax = dir_ax
        print("Best axis")
        print(best_ax)
        print("Max difference")
        print(max_difference)
        return directed_axis_collection[best_ax]['note_vector']

class SignatureOfFifthsUtility:
    """
        The function now counts the pitches frequency on the basis of the number of track's messages that
        have certain pitch's code - the more messages the more the note.
    """

    def count_notes_in_track(self, track) -> {}:
        msg_types = []
        notes = self.initialize_empty_notes_dict()
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

    def initialize_empty_notes_dict(self):
        return  Counter({Note.C: 0, Note.C_SHARP: 0, Note.D: 0, Note.D_SHARP: 0, Note.E: 0, Note.F: 0, Note.F_SHARP: 0,
                 Note.G: 0, Note.G_SHARP: 0, Note.A: 0, Note.A_SHARP: 0, Note.B: 0})
    def calculate_signature_of_fifths(self, notes) -> SignatureOfFifths:
        signature = SignatureOfFifths()
        for name, value in zip(notes.keys(), notes.values()):
            signature.signature[Note(name)].length = value / max(notes.values()) if max(notes.values()) != 0 else 0
        return signature

    def calculate_cvsf(self, signature: SignatureOfFifths):
        cvsf_vector = add_vector_list(
            list((note_vector.length, note_vector.direction) for note_vector in signature.signature.values()))
        cvsf = NoteVector(cvsf_vector[0], cvsf_vector[1])
        signature.cvsf = cvsf
        return signature

    def calculate_mdasf(self, signature: SignatureOfFifths):
        creator = DirectedAxisCreator()
        mdasf = creator.determine_from_signature(signature)
        signature.mdasf = mdasf
        return signature

    def calculate_mode_angle(self, signature: SignatureOfFifths):
        angle_one = (signature.mdasf.direction + 90.0) % 360
        angle_sf = signature.cvsf.direction % 360
        print("angle one")
        print(angle_one)
        print("angle_sf")
        print(angle_sf)
        mode_angle = angle_one - angle_sf
        print("mode_angle")
        print(mode_angle)
        signature.mode_angle = mode_angle
        return signature

    def get_tonation_pointed_by_mdasf(self, signature: SignatureOfFifths):
        tonation_pointed_by_mdasf = NoteVectorDirection((signature.mdasf.direction + 30.0) % 360)
        return Note.from_string(tonation_pointed_by_mdasf.name)

    def calculate_tonation_with_mode_axis(self, signature: SignatureOfFifths) -> Tonation:
        tonation_pointed_by_mdasf = NoteVectorDirection((signature.mdasf.direction + 30.0) % 360)
        self.calculate_mode_angle(signature)
        print("tonation pointed by mdasf")
        print(tonation_pointed_by_mdasf)
        print("mode angle")
        print(signature.mode_angle)
        tonation = Tonation(note=tonation_pointed_by_mdasf, mode=Mode.MAJOR)
        if signature.mode_angle < 0:
            tonation.mode = Mode.MINOR
        print(tonation)
        return tonation
        # elif algorithms.mode_angle == 0:
        #     pass
