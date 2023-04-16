import numpy as np
from signature_of_fifths_algorithm import Note, Mode
from model.definitions import Profile, TONAL_PROFILES, KS_PROFILE_MAJOR, KS_PROFILE_MINOR, T_PROFILE_MAJOR, T_PROFILE_MINOR, AS_PROFILE_MAJOR, AS_PROFILE_MINOR

def calculate_pearson_correlation(sample_vector, reference_vector):
    if len(sample_vector) != len(reference_vector):
        return 0.0
    return np.corrcoef(sample_vector, reference_vector)

def get_tonal_profile(tonation_note:Note, tonation_mode:Mode, profile:Profile):
    base_profile =  TONAL_PROFILES[(profile,tonation_mode)]
    for _ in range(0, tonation_note.value):
        base_profile.append(base_profile.pop(0))
    return base_profile


def calculate_correlation_with_tonal_profile(sample_vector, tonation_note:Note, tonation_mode:Mode, profile:Profile):
    return calculate_pearson_correlation(sample_vector, get_tonal_profile(tonation_note, tonation_mode, profile))


def classic_tonal_profiles_algorithm(sample_vector, profile:Profile):
    max_correlation = 0.0
    best_matched_tonation = [Note.C, Mode.MAJOR]
    for note in Note:
        major = calculate_correlation_with_tonal_profile(sample_vector, note, Mode.MAJOR, profile)
        minor = calculate_correlation_with_tonal_profile(sample_vector, note, Mode.MINOR, profile)
        if major > max_correlation:
            max_correlation = major
            best_matched_tonation = [note, Mode.MAJOR]
        if minor > max_correlation:
            max_correlation = minor
            best_matched_tonation = [note, Mode.MINOR]
    return best_matched_tonation

def decide_between_parallel(sample_vector, tonation_note:Note, profile:Profile):
    major = calculate_correlation_with_tonal_profile(sample_vector, tonation_note, Mode.MAJOR, profile)
    parallel_tonation = tonation_note.value - 3
    if parallel_tonation < 0:
        parallel_tonation = 12 + parallel_tonation
    minor = calculate_correlation_with_tonal_profile(sample_vector, Note(parallel_tonation), Mode.MINOR, profile)

    if minor > major:
        return [Note(parallel_tonation), Mode.MINOR]
    else:
        return [tonation_note, Mode.MAJOR]



