from model.definitions import Note, Mode


def create_tonation_string(tonation_note, tonation_mode: Mode):
    tonation_name = ''

    if tonation_note.name == Note.C.name:
        tonation_name = 'C'
    elif tonation_note.name == Note.G.name:
        tonation_name = 'G'
    elif tonation_note.name == Note.D.name:
        tonation_name = 'D'
    elif tonation_note.name == Note.A.name:
        tonation_name = 'A'
    elif tonation_note.name == Note.E.name:
        tonation_name = 'E'
    elif tonation_note.name == Note.B.name:
        tonation_name = 'B'
    elif tonation_note.name == Note.F_SHARP.name:
        tonation_name = 'F#'
    elif tonation_note.name == Note.C_SHARP.name:
        tonation_name = 'C#'
    elif tonation_note.name == Note.G_SHARP.name:
        tonation_name = 'A♭'
    elif tonation_note.name == Note.D_SHARP.name:
        tonation_name = 'E♭'
    elif tonation_note.name == Note.A_SHARP.name:
        tonation_name = 'B♭'
    elif tonation_note.name == Note.F.name:
        tonation_name = 'F'

    mode = "major"
    if tonation_mode.name == Mode.MINOR.name:
        mode = "minor"

    return tonation_name + " " + mode
