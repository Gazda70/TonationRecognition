import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QGraphicsScene, QGraphicsView
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QTransform
from PyQt5.QtCore import Qt

from midi_handling.midi_reader import MidiReader

FILE_LOAD_PAGE = "file_load.ui"
SIGNATURE_DISPLAY_PAGE = "signature_display.ui"

class UI_FileLoadingPage(QMainWindow):
    def __init__(self):
        super(UI_FileLoadingPage, self).__init__()

        uic.loadUi(FILE_LOAD_PAGE, self)
        #https://www.youtube.com/watch?v=gg5TepTc2Jg
        self.open_file_button = self.findChild(QPushButton, "openFileButton")
        self.open_file_button.clicked.connect(self.open_file_button_clicker)

        self.calculate_signature_button = self.findChild(QPushButton, "calculateSignatureButton")
        self.calculate_signature_button.clicked.connect(self.calculate_signature_button_clicker)

        self.show()


    def open_file_button_clicker(self):
        fname = QFileDialog.getOpenFileName()
        print(fname[0])
        self.read_midi(fname[0])

    def read_midi(self, filename):
        reader = MidiReader()
        reader.read_file(filename)

    def calculate_signature_button_clicker(self):
        self.change_to_signature_display_page()

    def change_to_signature_display_page(self):
        widget.setCurrentWidget(signature_display_page)
        widget.currentWidget().draw_signature_graphics_view()


class UI_SignatureDisplayPage(QMainWindow):
    def __init__(self):
        super(UI_SignatureDisplayPage, self).__init__()
        uic.loadUi(SIGNATURE_DISPLAY_PAGE, self)

        self.signature_graphics_view = self.findChild(QGraphicsView, "signatureGraphicsView")

        self.show()

    def change_to_file_loading_page(self):
        widget.setCurrentWidget(file_loading_page)

    def draw_signature_graphics_view(self):
        scene = QGraphicsScene()

        brush = QBrush(Qt.green)

        pen = QPen(Qt.red)

        self.signature_graphics_view.setScene(scene)

        rec_start_x = -200
        rec_start_y = -200
        rec_end_x = 400
        rec_end_y = 400
        scene.addEllipse(rec_start_x, rec_start_y, rec_end_x, rec_end_y, pen, brush)

        for angle in range(0, 360, 30):
            transform = QTransform()
            line = scene.addLine(0, 0, 0, rec_start_y, pen)
            transform.rotate(angle)
            line.setTransform(transform)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
file_loading_page = UI_FileLoadingPage()
widget.addWidget(file_loading_page)
signature_display_page = UI_SignatureDisplayPage()
widget.addWidget(signature_display_page)
w = 800
h = 500
widget.resize(w, h)
widget.show()
app.exec_()