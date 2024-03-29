from PyQt5.QtGui import QBrush, QPen, QTransform, QFont, QPainterPath, QPolygonF, QPainter, QPolygon
from PyQt5.QtCore import Qt, QPointF, QRect, QRectF
from PyQt5 import QtWidgets
from model.definitions import SignatureOfFifths
from algorithms.signature_of_fifths_algorithm import SignatureOfFifthsUtility
import math

TONATION_NAMES = ['C', 'G', 'D', 'A', 'E', 'H', 'F#', 'D♭', 'A♭', 'E♭', 'B', 'F']


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
        self.scene.addEllipse(self.rec_start_x, self.rec_start_y, self.rec_end_x, self.rec_end_y, self.pen)

        for angle, note in zip(range(0, 360, 30), TONATION_NAMES):
            textTransform = QTransform()
            text = self.scene.addText(note)

            textTransform.rotate(angle)
            move = self.rec_start_y - 20
            textTransform.translate(-7, move)
            text.setTransform(textTransform)

class SignatureGraphic:
    def __init__(self, signature_of_fifths: SignatureOfFifths, signature_graphics_view, scene):
        self.signature_of_fifths = signature_of_fifths
        self.signature_graphics_view = signature_graphics_view
        self.scene = scene
        self.signature_graphics_view.setScene(self.scene)
        self.brush = QBrush(Qt.green)
        self.pen = QPen(Qt.blue)
        self.font = QFont("Helvetica", 24)
        self.rec_start_x = -200
        self.rec_start_y = -200
        self.rec_end_x = 400
        self.rec_end_y = 400
        self.sig_util = SignatureOfFifthsUtility()

    def draw_vector_per_note(self):
        for name, value in zip(self.signature_of_fifths.signature.keys(), self.signature_of_fifths.signature.values()):
            self.draw_vector(value.length, value.direction, QPen(Qt.blue))

    def draw_cvsf(self):
        self.draw_vector(1, self.signature_of_fifths.cvsf.direction, QPen(Qt.black, 5))


    def arrowCalc(self, start_point=None, end_point=None):  # calculates the point where the arrow should be drawn
        arrow_height = 20
        arrow_width = 10
        try:
            startPoint, endPoint = start_point, end_point

            dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()

            leng = math.sqrt(dx ** 2 + dy ** 2)
            normX, normY = dx / leng, dy / leng  # normalize

            # perpendicular vector
            perpX = -normY
            perpY = normX

            leftX = endPoint.x() + arrow_height * normX + arrow_width * perpX
            leftY = endPoint.y() + arrow_height * normY + arrow_width * perpY

            rightX = endPoint.x() + arrow_height * normX - arrow_width * perpX
            rightY = endPoint.y() + arrow_height * normY - arrow_width * perpY

            point2 = QPointF(leftX, leftY)
            point3 = QPointF(rightX, rightY)

            return QPolygonF([point2, endPoint, point3])

        except (ZeroDivisionError, Exception):
            return None

    def draw_vector(self, vector_magnitude, vector_angle, pen: QPen, text_to_display=None):
        note_vector_length_normalised = vector_magnitude * self.rec_start_y
        note_vector_direction = vector_angle
        transform = QTransform()
        line = self.scene.addLine(0, 0, 0, note_vector_length_normalised, pen)
        transform.rotate(note_vector_direction)
        line.setTransform(transform)
        if text_to_display != None:
            textTransform = QTransform()
            text = self.scene.addText(text_to_display)
            textTransform.rotate(vector_angle)
            move = self.rec_start_y + 50
            textTransform.translate(40, move)
            textTransform.rotate(-vector_angle)
            text.setTransform(textTransform)

    def draw_vector_with_arrow(self, vector_magnitude, vector_angle, pen: QPen, arrow_pen:QPen, arrow_brush:QBrush, text_to_display=None):
        note_vector_length_normalised = vector_magnitude * self.rec_start_y
        note_vector_direction = vector_angle
        transform = QTransform()
        line = self.scene.addLine(0, 0, 0, note_vector_length_normalised, pen)
        transform.rotate(note_vector_direction)
        line.setTransform(transform)

        arrow = self.arrowCalc(QPointF(0.0, 0.0), QPointF(0.0, note_vector_length_normalised))  # change path.PointAtPercent() value to move arrow on the line
        arrow_polygon = self.scene.addPolygon(arrow, arrow_pen, arrow_brush)
        arrow_polygon.setTransform(transform)
        textTransform = QTransform()
        if text_to_display != None:
            text = self.scene.addText(text_to_display)

            textTransform.rotate(vector_angle)
            move = self.rec_start_y + 50
            textTransform.translate(20, move)
            textTransform.rotate(-vector_angle)
            text.setTransform(textTransform)

    def draw_mdasf(self):
        self.draw_vector(1.0, self.signature_of_fifths.mdasf.direction - 180.0, QPen(Qt.red, 3, Qt.DashLine))
        self.draw_vector_with_arrow(1.0, self.signature_of_fifths.mdasf.direction, QPen(Qt.red, 3, Qt.DashLine), QPen(Qt.red, 3), QBrush(Qt.red))

    def draw_major_minor_mode_axis(self):
        mode_axis_angle = self.signature_of_fifths.mdasf.direction + 90.0
        self.draw_vector(1.0, mode_axis_angle - 180.0, QPen(Qt.green, 3, Qt.DashLine))
        self.draw_vector_with_arrow(1.0, mode_axis_angle, QPen(Qt.green, 3, Qt.DashLine), QPen(Qt.green, 3), QBrush(Qt.green))

    def draw_tonal_profiles_results(self, ks_results, as_results, t_results):
        textTransform = QTransform()
        textTransform.translate(-200, 300)
        first_text = self.scene.addText("Krumhansl-Schmuckler: " + ks_results)
        first_text.setTransform(textTransform)
        textTransform = QTransform()
        textTransform.translate(-200, 320)
        second_text = self.scene.addText("Albrecht-Schanachan: " + as_results)
        second_text.setTransform(textTransform)
        textTransform = QTransform()
        textTransform.translate(-200, 340)
        third_text = self.scene.addText("Temperley: " + t_results)
        third_text.setTransform(textTransform)

    def draw_legend(self):
        brush = QBrush(Qt.blue)
        pen = QPen(Qt.blue)
        textTransform = QTransform()
        textTransform.translate(100, 280)
        first_text = self.scene.addText("Signature vectors")
        first_text.setTransform(textTransform)
        self.scene.addPolygon(QPolygonF(QRectF(80.0, 287.0, 20.0, 10.0)), pen, brush)

        brush = QBrush(Qt.red)
        pen = QPen(Qt.red)
        textTransform = QTransform()
        textTransform.translate(100, 300)
        first_text = self.scene.addText("Main axis")
        first_text.setTransform(textTransform)
        self.scene.addPolygon(QPolygonF(QRectF(80.0, 307.0, 20.0, 10.0)), pen, brush)

        brush = QBrush(Qt.black)
        pen = QPen(Qt.black)
        textTransform = QTransform()
        textTransform.translate(100, 320)
        second_text = self.scene.addText("Characteristic vector")
        second_text.setTransform(textTransform)
        self.scene.addPolygon(QPolygonF(QRectF(80.0, 327.0, 20.0, 10.0)), pen, brush)

        brush = QBrush(Qt.green)
        pen = QPen(Qt.green)
        textTransform = QTransform()
        textTransform.translate(100, 340)
        third_text = self.scene.addText("Mode axis")
        third_text.setTransform(textTransform)
        self.scene.addPolygon(QPolygonF(QRectF(80.0, 347.0, 20.0, 10.0)), pen, brush)