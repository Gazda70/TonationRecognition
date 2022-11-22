import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QGraphicsScene, QGraphicsView
from PyQt5 import uic, QtWidgets

from midi_handling.midi_reader import MidiReader

from signature_drawing import CircleOfFifths, SignatureGraphic

FILE_LOAD_PAGE = "file_load.ui"
SIGNATURE_DISPLAY_PAGE = "signature_display.ui"


class UI_FileLoadingPage(QMainWindow):
    def __init__(self):
        super(UI_FileLoadingPage, self).__init__()

        uic.loadUi(FILE_LOAD_PAGE, self)
        # https://www.youtube.com/watch?v=gg5TepTc2Jg
        self.open_file_button = self.findChild(QPushButton, "openFileButton")
        self.open_file_button.clicked.connect(self.open_file_button_clicker)

        self.calculate_signature_button = self.findChild(QPushButton, "calculateSignatureButton")
        self.calculate_signature_button.clicked.connect(self.calculate_signature_button_clicker)

        self.list_of_signatures = None

        self.show()

    def open_file_button_clicker(self):
        fname = QFileDialog.getOpenFileName()
        print(fname[0])
        self.read_midi(fname[0])

    def read_midi(self, filename):
        reader = MidiReader()
        self.list_of_signatures = reader.read_file(filename)
        print(self.list_of_signatures)

    def calculate_signature_button_clicker(self):
        self.change_to_signature_display_page()

    def change_to_signature_display_page(self):
        widget.setCurrentWidget(signature_display_page)
        widget.currentWidget().set_list_of_signatures(self.list_of_signatures)
        widget.currentWidget().draw_signature_graphics_view()


class UI_SignatureDisplayPage(QMainWindow):
    def __init__(self):
        super(UI_SignatureDisplayPage, self).__init__()
        uic.loadUi(SIGNATURE_DISPLAY_PAGE, self)

        self.signature_graphics_view = self.findChild(QGraphicsView, "signatureGraphicsView")
        self.return_button = self.findChild(QPushButton, "returnButton")
        self.return_button.clicked.connect(self.return_to_file_loading_page)

        self.scene = QGraphicsScene()
        self.list_of_signatures = None

        self.show()

    def set_list_of_signatures(self, list_of_signatures):
        self.list_of_signatures = list_of_signatures

    def change_to_file_loading_page(self):
        widget.setCurrentWidget(file_loading_page)

    def draw_signature_graphics_view(self):
        circle_of_fifths = CircleOfFifths(self.signature_graphics_view, self.scene)
        circle_of_fifths.draw()
        #CHECK IF THE TRACK CONTAINS ANY NOTES, IN OTHER CASE THIS OPERATION MAKES NO SENSE AND DIVIDES BY 0
        print("self.list_of_signatures[3]")
        print(self.list_of_signatures[3])
        signature_graphic = SignatureGraphic(signature_of_fifths=self.list_of_signatures[1], #THIS IS ARBITRAL CHOICE, MECHANISM FOR TRACKS HANDLING NEEDED
                                             signature_graphics_view=self.signature_graphics_view, scene=self.scene)
        signature_graphic.draw_vector_per_note()
        signature_graphic.draw_cvsf()
        signature_graphic.draw_mdasf()

    def return_to_file_loading_page(self):
        widget.setCurrentWidget(file_loading_page)


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
