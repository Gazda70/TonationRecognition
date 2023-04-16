from algorithms.signature_of_fifths_algorithm import SignatureOfFifthsUtility
from model.definitions import AlgorithmInfo, Algorithm
from utils.mappings import create_tonation_string

class AlgorithmManager:
    def __init__(self):
        self.signature_utility = SignatureOfFifthsUtility()

    def execute_algorithm(self, algorithm_info:AlgorithmInfo, note_dict):
        if algorithm_info.algorithm_type == Algorithm.SIGNATURE_MODE_AXIS:
            signature = self.basic_signature_algorithm(note_dict)
            tonation = self.signature_utility.calculate_tonation_with_mode_axis(signature)
            return create_tonation_string(tonation_note=tonation.note, tonation_mode=tonation.mode), signature

    def basic_signature_algorithm(self, notes_dict):
        signature = self.signature_utility.calculate_signature_of_fifths(notes_dict)
        self.signature_utility.calculate_cvsf(signature)
        self.signature_utility.calculate_mdasf(signature)
        return signature


    def get_tonation_information(self):
        return self.signature_utility.calculate_tonation(self.signature_of_fifths)