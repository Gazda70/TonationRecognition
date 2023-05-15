from enum import Enum
from dataclasses import dataclass

NOTE_VECTOR_MAX_LENGTH = 2

FILE_LOAD_PAGE = "file_load.ui"
SIGNATURE_DISPLAY_PAGE = "signature_display.ui"
MAIN_UI_PAGE = "main_window.py"

MIDI_FILES_PATH = "E:\\PracaMagisterska\\TonationRecognition\\midi_files"

KS_PROFILE_MAJOR = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
KS_PROFILE_MINOR = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 2.98, 2.69, 3.34, 3.17]
T_PROFILE_MAJOR = [0.75, 0.06, 0.49, 0.08, 0.67, 0.46, 0.10, 0.72, 0.10, 0.37, 0.06, 0.40]
T_PROFILE_MINOR = [0.71, 0.08, 0.48, 0.62, 0.05, 0.46, 0.11, 0.75, 0.40, 0.07, 0.13, 0.33]
AS_PROFILE_MAJOR = [0.24, 0.01, 0.11, 0.01, 0.14, 0.09, 0.02, 0.21, 0.01, 0.08, 0.01, 0.08]
AS_PROFILE_MINOR = [0.22, 0.01, 0.10, 0.12, 0.02, 0.10, 0.01, 0.21, 0.06, 0.02, 0.06, 0.05]

class WindowModes(Enum):
    FROM_START, FROM_END = range(0, 2)


class Profile(Enum):
    KS, T, AS = range(0, 3)


TONAL_PROFILE_NAMES = {"Krumhansl-Schmuckler": Profile.KS, "Albrecht-Shanahan": Profile.AS, "Temperley": Profile.T}


class Mode(Enum):
    MAJOR, MINOR = range(2)


TONAL_PROFILES = {(Profile.KS, Mode.MAJOR): KS_PROFILE_MAJOR, (Profile.KS, Mode.MINOR): KS_PROFILE_MINOR,
                  (Profile.T, Mode.MAJOR): T_PROFILE_MAJOR, (Profile.T, Mode.MINOR): T_PROFILE_MINOR,
                  (Profile.AS, Mode.MAJOR): AS_PROFILE_MAJOR, (Profile.AS, Mode.MINOR): AS_PROFILE_MINOR, }


class Algorithm(Enum):
    SIGNATURE_MODE_AXIS, SIGNATURE_TONAL_PROFILES, CLASSIC_TONAL_PROFILES = range(0, 3)


ALGORITHM_NAMES = {"Major/minor axis": Algorithm.SIGNATURE_MODE_AXIS,
                   "Tonal profiles": Algorithm.SIGNATURE_TONAL_PROFILES,
                   "Only tonal profiles": Algorithm.CLASSIC_TONAL_PROFILES}


class SampleMode(Enum):
    QUANTITY = 1
    DURATION = 2


SAMPLE_CALCULATION_MODES = {"Notes quantity": SampleMode.QUANTITY, "Notes duration": SampleMode.DURATION}

class RhythmicValues(Enum):
    WHOLE = 1
    HALF = 2
    QUARTER = 4
    EIGHT = 8
    SIXTEEN = 16
    THIRTY_TWO = 32
    SIXTY_FOUR = 64
    LOWER_THAN_SIXTY_FOUR = 65

RHYTHMIC_VALUES = {"WHOLE": RhythmicValues.WHOLE, "HALF": RhythmicValues.HALF, "QUARTER":RhythmicValues.QUARTER, "EIGHT":RhythmicValues.EIGHT,
                  "SIXTEEN": RhythmicValues.SIXTEEN, "THIRTY_TWO":RhythmicValues.THIRTY_TWO, "SIXTY_FOUR":RhythmicValues.SIXTY_FOUR}


@dataclass
class AlgorithmInfo:
    algorithm_type: Algorithm
    sample_calculation_mode: SampleMode
    profile: Profile


class Note(Enum):
    C, C_SHARP, D, D_SHARP, E, F, F_SHARP, G, G_SHARP, A, A_SHARP, B = range(12)

    @staticmethod
    def from_string(note_string):
        NOTES = {"C": Note.C, "C_SHARP": Note.C_SHARP, "D": Note.D, "D_SHARP": Note.D_SHARP, "E": Note.E, "F": Note.F,
                 "F_SHARP": Note.F_SHARP, "G": Note.G,
                 "G_SHARP": Note.G_SHARP, "A": Note.A, "A_SHARP": Note.A_SHARP, "B": Note.B}
        return NOTES[note_string]


class NoteVectorDirection(Enum):
    C, G, D, A, E, B, F_SHARP, C_SHARP, G_SHARP, D_SHARP, A_SHARP, F = range(0, 360, 30)


@dataclass
class Tonation:
    note: NoteVectorDirection
    mode: Mode


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


@dataclass
class NoteVector:
    length: float
    direction: float


@dataclass
class SignatureOfFifths:
    def __init__(self):
        self.signature = {Note.A: NoteVector(0, NoteVectorDirection.A.value),
                          Note.D: NoteVector(0, NoteVectorDirection.D.value),
                          Note.G: NoteVector(0, NoteVectorDirection.G.value),
                          Note.C: NoteVector(0, NoteVectorDirection.C.value),
                          Note.F: NoteVector(0, NoteVectorDirection.F.value),
                          Note.C_SHARP: NoteVector(0, NoteVectorDirection.C_SHARP.value),
                          Note.D_SHARP: NoteVector(0, NoteVectorDirection.D_SHARP.value),
                          Note.E: NoteVector(0, NoteVectorDirection.E.value),
                          Note.F_SHARP: NoteVector(0, NoteVectorDirection.F_SHARP.value),
                          Note.G_SHARP: NoteVector(0, NoteVectorDirection.G_SHARP.value),
                          Note.A_SHARP: NoteVector(0, NoteVectorDirection.A_SHARP.value),
                          Note.B: NoteVector(0, NoteVectorDirection.B.value)}

        self.cvsf: NoteVector = None
        self.mdasf: NoteVector = None
        self.mode_angle: float = 0.0
        self.tonation: Tonation = None

    def is_empty(self):
        for note in self.signature.values():
            if note.length != 0:
                return False
        return True

class SignatureCalculationMode(Enum):
    QUANTITY, DURATION = range(2)


@dataclass
class RhythmicValuesDuration:
    WHOLE: int
    HALF: int
    QUARTER: int
    EIGHT: int
    SIXTEEN: int
    THIRTY_TWO: int
    SIXTY_FOUR: int


@dataclass
class RawElement:
    is_chord: bool
    is_pause: bool
    start_notes: []
    end_notes: []
    control: []
    raw_duration: int  # total duration represented as integer

'''
A note or group of notes that have the same duration
'''
@dataclass
class ProcessedElement:
    is_chord: bool  # if the element is a chord, i.e. if more than one note is played simultaneously
    notes: []  # total duration represented as collection of notes
    raw_duration: int  # total duration represented as integer


@dataclass
class NoteWithDuration:
    note: Note
    is_pause: bool
    duration: [] #list of RhythmicValues


@dataclass
class ProcessedTrack:
    elements: []


@dataclass
class Tempo:
    tempo: int
    start_time: int

@dataclass
class RhythmicValuesDurationWithStartTime:
    rhythmic_values_duration: RhythmicValuesDuration
    start_time: int