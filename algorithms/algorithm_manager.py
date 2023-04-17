from algorithms.signature_of_fifths_algorithm import SignatureOfFifthsUtility
from model.definitions import AlgorithmInfo, Algorithm
from utils.mappings import create_tonation_string
from algorithms.tonal_profiles_algorithm import TonalProfilesUtility


class AlgorithmManager:
    def __init__(self):
        self.signature_utility = SignatureOfFifthsUtility()
        self.tonal_profiles_utility = TonalProfilesUtility()

    def execute_algorithm(self, algorithm_info: AlgorithmInfo, note_dict):
        result_note, result_mode = None, None
        signature = None
        if algorithm_info.algorithm_type == Algorithm.SIGNATURE_MODE_AXIS:
            signature = self.basic_signature_algorithm(note_dict)
            tonation = self.signature_utility.calculate_tonation_with_mode_axis(signature)
            result_note, result_mode = tonation.note, tonation.mode
        elif algorithm_info.algorithm_type == Algorithm.SIGNATURE_TONAL_PROFILES:
            signature = self.basic_signature_algorithm(note_dict)
            tonation_note = self.signature_utility.get_tonation_pointed_by_mdasf(signature)
            result_note, result_mode = self.tonal_profiles_utility.decide_between_parallel(sample_vector=note_dict,
                                                                                           tonation_note=tonation_note,
                                                                                           profile=algorithm_info.profile)
        elif algorithm_info.algorithm_type == Algorithm.CLASSIC_TONAL_PROFILES:
            result_note, result_mode = self.tonal_profiles_utility.classic_tonal_profiles_algorithm(
                sample_vector=note_dict, profile=algorithm_info.profile)
        return create_tonation_string(tonation_note=result_note, tonation_mode=result_mode), signature

    def basic_signature_algorithm(self, notes_dict):
        signature = self.signature_utility.calculate_signature_of_fifths(notes_dict)
        self.signature_utility.calculate_cvsf(signature)
        self.signature_utility.calculate_mdasf(signature)
        return signature

    def get_tonation_information(self):
        return self.signature_utility.calculate_tonation(self.signature_of_fifths)
