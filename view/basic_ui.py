import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QGraphicsScene, QGraphicsView, \
    QComboBox, QListWidget, QListWidgetItem, QListView
from PyQt5 import uic, QtWidgets

from midi_handling.midi_reader import MidiReader

from signature_drawing import CircleOfFifths, SignatureGraphic

FILE_LOAD_PAGE = "file_load.ui"
SIGNATURE_DISPLAY_PAGE = "signature_display.ui"
MAIN_UI_PAGE="main_window.ui"

MIDI_FILES_PATH="E:\\PracaMagisterska\\TonationRecognition\\midi_files"

class UI_MainPage(QMainWindow):
    def __init__(self):
        super(UI_MainPage, self).__init__()

        uic.loadUi(MAIN_UI_PAGE, self)
        # https://www.youtube.com/watch?v=gg5TepTc2Jg
        self.load_file_button = self.findChild(QPushButton, "load_files_button")
        self.load_file_button.clicked.connect(self.load_file_button_clicker)

        self.save_results_button = self.findChild(QPushButton, "save_results_button")
        self.save_results_button.clicked.connect(self.save_results_button_clicker)

        self.algorithm_type_dropdown = self.findChild(QComboBox, "algorithm_type_dropdown")
        self.algorithm_type_dropdown.addItem("Signature of fifths")

        self.method_details_dropdown = self.findChild(QComboBox, "signature_calculation_mode")
        self.method_details_dropdown.addItems(["Notes quantity", "Notes duration"])

        self.method_details_dropdown = self.findChild(QComboBox, "tonal_profiles_type")

        self.midi_channel_dropdown = self.findChild(QComboBox, "midi_channel_dropdown")

        self.calculate_signature_button = self.findChild(QPushButton, "calculate_button")
        self.calculate_signature_button.clicked.connect(self.calculate_button_clicker)

        self.signature_graphics_view = self.findChild(QGraphicsView, "signature_graphic_view")

        self.track_list = self.findChild(QListWidget, "track_list")

        self.scene = QGraphicsScene()

        self.list_of_signatures = None

        self.show()

    def load_file_button_clicker(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open MIDI file", MIDI_FILES_PATH, "MIDI files (*.mid);;")
        print(filename)
        if filename:
            self.read_midi(filename)

    def read_midi(self, filename):
        reader = MidiReader()
        self.list_of_signatures = reader.read_file(filename)
        print(self.list_of_signatures)
        self.setup_track_list()

    def setup_track_list(self):
        print("LIST LENGTH: " + str(len(self.list_of_signatures)))
        self.track_list.clear()
        self.track_list.addItems(["Track " + str(track_number + 1) for track_number in range(0, len(self.list_of_signatures))])


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

    def save_results_button_clicker(self):
        pass

    def calculate_button_clicker(self):
        self.draw_signature_graphics_view()


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
main_ui_page = UI_MainPage()
widget.addWidget(main_ui_page)
w = 1200
h = 900
widget.resize(w, h)
widget.show()
app.exec_()
