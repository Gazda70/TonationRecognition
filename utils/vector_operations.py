import numpy as np

from signature.signature_of_fifths_functions import NoteVector


def add_two_vectors(vector_one: NoteVector, vector_two: NoteVector) -> NoteVector:
    vector_one_angle_radians = np.deg2rad(vector_one.direction)
    vector_two_angle_radians = np.deg2rad(vector_two.direction)

    vector_one_xy = np.array([vector_one.length * np.cos(vector_one_angle_radians),
                             vector_one.length * np.sin(vector_one_angle_radians)])

    vector_two_xy = np.array([vector_two.length * np.cos(vector_two_angle_radians),
                             vector_two.length * np.sin(vector_two_angle_radians)])

    resultant_xy = vector_one_xy + vector_two_xy

    resultant_length = np.sqrt(resultant_xy[0] ** 2 + resultant_xy[1] ** 2)

    resultant_angle = np.rad2deg(np.arccos(resultant_xy[0]/resultant_length))

    if resultant_xy[1] < 0:
        resultant_angle *= -1

    return NoteVector(resultant_length, resultant_angle)