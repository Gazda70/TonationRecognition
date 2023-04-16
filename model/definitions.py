from enum import Enum
from dataclasses import dataclass


NOTE_VECTOR_MAX_LENGTH = 2

FILE_LOAD_PAGE = "file_load.ui"
SIGNATURE_DISPLAY_PAGE = "signature_display.ui"
MAIN_UI_PAGE="main_window.ui"

MIDI_FILES_PATH="E:\\PracaMagisterska\\TonationRecognition\\midi_files"

ALGORITHM_NAMES = ["Signature of fifths", "Tonal profiles"]
SAMPLE_CALCULATION_MODES = ["Notes quantity", "Notes duration"]
TONAL_PROFILE_NAMES = ["Krumhansl-Schmuckler", "Albrecht-Shanahan", "Temperley"]


KS_PROFILE_MAJOR=[6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
KS_PROFILE_MINOR=[6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 2.98, 2.69, 3.34, 3.17]
T_PROFILE_MAJOR=[0.75, 0.06, 0.49, 0.08, 0.67, 0.46, 0.10, 0.72, 0.10, 0.37, 0.06, 0.40]
T_PROFILE_MINOR=[0.71, 0.08, 0.48, 0.62, 0.05, 0.46, 0.11, 0.75, 0.40, 0.07, 0.13, 0.33]
AS_PROFILE_MAJOR=[0.24, 0.01, 0.11, 0.01, 0.14, 0.09, 0.02, 0.21, 0.01, 0.08, 0.01, 0.08]
AS_PROFILE_MINOR=[0.22, 0.01, 0.10, 0.12, 0.02, 0.10, 0.01, 0.21, 0.06, 0.02, 0.06, 0.05]

class Profiles(Enum):
    KS, T, AS = range(0,3)

class Mode(Enum):
    MAJOR, MINOR = range(2)

TONAL_PROFILES={(Profiles.KS, Mode.MAJOR):KS_PROFILE_MAJOR, (Profiles.KS, Mode.MINOR):KS_PROFILE_MINOR,
                (Profiles.T, Mode.MAJOR):T_PROFILE_MAJOR, (Profiles.T, Mode.MINOR):T_PROFILE_MINOR,
                (Profiles.AS, Mode.MAJOR):AS_PROFILE_MAJOR, (Profiles.AS, Mode.MINOR):AS_PROFILE_MINOR,}

class Algorithm(Enum):
    SIGNATURE_MODE_AXIS, SIGNATURE_TONAL_PROFILES, CLASSIC_TONAL_PROFILES = range(0, 3)


class SampleMode(Enum):
    QUANTITY=1
    DURATION=2

@dataclass
class AlgorithmInfo:
    algorithm_type:Algorithm
    sample_calculation_mode:SampleMode


class Note(Enum):
    C, C_SHARP, D, D_SHARP, E, F, F_SHARP, G, G_SHARP, A, A_SHARP, B = range(12)

class NoteVectorDirection(Enum):
    C_DIR, G_DIR, D_DIR, A_DIR, E_DIR, B_DIR , F_SHARP_DIR, C_SHARP_DIR, G_SHARP_DIR, D_SHARP_DIR , A_SHARP_DIR, F_DIR = \
        range(0, 360, 30)

@dataclass
class Tonation:
    note:NoteVectorDirection
    mode:Mode

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

        self.cvsf:NoteVector = None
        self.mdasf:NoteVector = None
        self.mode_angle:float = 0.0
        self.tonation:Tonation = None

class SignatureCalculationMode(Enum):
    QUANTITY, DURATION = range(2)

class NotesDuration(Enum):
    WHOLE=1
    HALF=2
    QUARTER=4
    EIGHT=8
    SIXTEEN=16
    THIRTY_TWO=32
    SIXTY_FOUR=64

class RhytmicValues(Enum):
    WHOLE=1
    HALF=2
    QUARTER=4
    EIGHT=8
    SIXTEEN=16
    THIRTY_TWO=32
    SIXTY_FOUR=64
    LOWER_THAN_SIXTY_FOUR=65

@dataclass
class RhytmicValuesDuration:
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
    is_chord: bool # if the element is a chord, i.e. if more than one note is played simultaneously
    notes: [] # total duration represented as collection of notes
    raw_duration: int   # total duration represented as integer

@dataclass
class NoteWithDuration:
    note: Note
    is_pause: bool
    duration: RhytmicValues

@dataclass
class ProcessedTrack:
    elements: []

@dataclass
class Tempo:
    tempo:int
    start_time:int