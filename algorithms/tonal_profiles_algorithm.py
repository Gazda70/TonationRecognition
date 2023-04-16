import numpy as np
from signature_of_fifths_algorithm import Note, Mode

KS_PROFILE_MAJOR=[6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
KS_PROFILE_MINOR=[6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 2.98, 2.69, 3.34, 3.17]
T_PROFILE_MAJOR=[0.75, 0.06, 0.49, 0.08, 0.67, 0.46, 0.10, 0.72, 0.10, 0.37, 0.06, 0.40]
T_PROFILE_MINOR=[0.71, 0.08, 0.48, 0.62, 0.05, 0.46, 0.11, 0.75, 0.40, 0.07, 0.13, 0.33]
AS_PROFILE_MAJOR=[0.24, 0.01, 0.11, 0.01, 0.14, 0.09, 0.02, 0.21, 0.01, 0.08, 0.01, 0.08]
AS_PROFILE_MINOR=[0.22, 0.01, 0.10, 0.12, 0.02, 0.10, 0.01, 0.21, 0.06, 0.02, 0.06, 0.05]

class Profiles(Enum):
    KS, T, AS = range(0,3)

TONAL_PROFILES={[Profiles.KS, Mode.MAJOR]:KS_PROFILE_MAJOR, [Profiles.KS, Mode.MINOR]:KS_PROFILE_MINOR,
                [Profiles.T, Mode.MAJOR]:T_PROFILE_MAJOR, [Profiles.T, Mode.MINOR]:T_PROFILE_MINOR,
                [Profiles.AS, Mode.MAJOR]:AS_PROFILE_MAJOR, [Profiles.AS, Mode.MINOR]:AS_PROFILE_MINOR,}

def calculate_pearson_correlation(sample_vector, reference_vector):
    if len(sample_vector) != len(reference_vector):
        return 0.0
    return np.corrcoef(sample_vector, reference_vector)

def get_tonal_profile(tonation_note:Note, tonation_mode:Mode, profile:Profiles):
    base_profile =  TONAL_PROFILES[[profile,tonation_mode]]
    for _ in range(0, tonation_note.value):
        base_profile.append(base_profile.pop(0))
    return base_profile


def calculate_correlation_with_tonal_profile(sample_vector, tonation_note:Note, tonation_mode:Mode, profile:Profiles):
    return calculate_pearson_correlation(sample_vector, get_tonal_profile(tonation_note, tonation_mode, profile))


def classic_tonal_profiles_algorithm(sample_vector, profile:Profiles):
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

def decide_between_parallel(sample_vector, tonation_note:Note, profile:Profiles):
    major = calculate_correlation_with_tonal_profile(sample_vector, tonation_note, Mode.MAJOR, profile)
    parallel_tonation = tonation_note.value - 3
    if parallel_tonation < 0:
        parallel_tonation = 12 + parallel_tonation
    minor = calculate_correlation_with_tonal_profile(sample_vector, Note(parallel_tonation), Mode.MINOR, profile)

    if minor > major:
        return [Note(parallel_tonation), Mode.MINOR]
    else:
        return [tonation_note, Mode.MAJOR]



