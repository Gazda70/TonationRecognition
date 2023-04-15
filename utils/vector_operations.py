import numpy as np
import math


def add_two_vectors(vector_one_magnitude, vector_one_angle, vector_two_magnitude, vector_two_angle) -> (float, float):
    vector_one_angle_radians = np.deg2rad(vector_one_angle)
    vector_two_angle_radians = np.deg2rad(vector_two_angle)

    vector_one_xy = np.array([vector_one_magnitude * np.cos(vector_one_angle_radians),
                             vector_one_magnitude * np.sin(vector_one_angle_radians)])

    vector_two_xy = np.array([vector_two_magnitude * np.cos(vector_two_angle_radians),
                             vector_two_magnitude * np.sin(vector_two_angle_radians)])

    resultant_xy = vector_one_xy + vector_two_xy

    resultant_length = np.sqrt(resultant_xy[0] ** 2 + resultant_xy[1] ** 2)

    resultant_angle = 0
    if not math.isnan(resultant_xy[0]) and not math.isnan(resultant_length) and resultant_length != 0:
        resultant_angle = np.rad2deg(np.arccos(resultant_xy[0]/resultant_length))

    if resultant_xy[1] < 0:
        resultant_angle *= -1

    return (resultant_length, resultant_angle)

def add_vector_list(vectors:[(float, int)]):
    result_vector = [vectors[0][0], vectors[0][1]]
    for vector in vectors[1:]:
        result_vector = add_two_vectors(result_vector[0], result_vector[1], vector[0], vector[1])
        print("result_vector")
        print(result_vector)
    return result_vector