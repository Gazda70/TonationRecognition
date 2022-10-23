import sys

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QBrush, QPen, QTransform, QFont
from PyQt5.QtCore import Qt
from signature.signature_of_fifths_functions import Note, NoteVectorDirection, NoteVector, SignatureOfFifths, SignatureOfFifthsUtility

TONATION_NAMES = ['C', 'G', 'D', 'A', 'E', 'H', 'F#', 'C#', 'A♭', 'E♭', 'B', 'F']

class CircleOfFifths:
    def __init__(self, signature_graphics_view, scene):

        self.signature_graphics_view = signature_graphics_view
        self.scene = scene
        self.signature_graphics_view.setScene(self.scene)
        self.brush = QBrush(Qt.green)
        self.pen = QPen(Qt.red)
        self.font = QFont("Helvetica", 24)
        self.rec_start_x = -200
        self.rec_start_y = -200
        self.rec_end_x = 400
        self.rec_end_y = 400

    def draw(self):
        self.scene.addEllipse(self.rec_start_x, self.rec_start_y, self.rec_end_x, self.rec_end_y, self.pen, self.brush)

        for angle, note in zip(range(0, 360, 30), TONATION_NAMES):
            transform = QTransform()
            line = self.scene.addLine(0, 0, 0, self.rec_start_y, self.pen)
            transform.rotate(angle)
            line.setTransform(transform)

            textTransform = QTransform()
            text = self.scene.addText(note)

            textTransform.rotate(angle)
            move = self.rec_start_y - 20
            textTransform.translate(0, move)
            #textTransform.rotate(360 - angle)
            text.setTransform(textTransform)


class SignatureGraphic:
    def __init__(self, signature_of_fifths: SignatureOfFifths, signature_graphics_view, scene):
        self.signature_of_fifths = signature_of_fifths
        self.signature_graphics_view = signature_graphics_view
        self.scene = scene
        self.signature_graphics_view.setScene(self.scene)
        self.brush = QBrush(Qt.green)
        self.pen = QPen(Qt.darkBlue)
        self.font = QFont("Helvetica", 24)
        self.rec_start_x = -200
        self.rec_start_y = -200
        self.rec_end_x = 400
        self.rec_end_y = 400

    def draw_vector_per_note(self):
        for name, value in zip(self.signature_of_fifths.signature.keys(), self.signature_of_fifths.signature.values()):
            note_vector_length_normalised = value.length * self.rec_start_y
            note_vector_direction = value.direction
            transform = QTransform()
            line = self.scene.addLine(0, 0, 0, note_vector_length_normalised, self.pen)
            transform.rotate(note_vector_direction)
            line.setTransform(transform)