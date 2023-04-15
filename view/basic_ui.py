import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QGraphicsScene, QGraphicsView, \
    QComboBox, QListWidget, QTextEdit, QListWidgetItem
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QColor

from file_manager.file_manager import MidiReader

from signature_drawing import CircleOfFifths, SignatureGraphic

from file_manager.track_manager import SignatureModes

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

        self.result_information = self.findChild(QTextEdit, "result_information")
        self.result_information.setReadOnly(True)

        self.notes_window_start = self.findChild(QTextEdit, "notes_window_start")

        self.notes_window_end = self.findChild(QTextEdit, "notes_window_end")

        self.notes_quantity_display = self.findChild(QTextEdit, "notes_quantity_display")

        self.notes_quantity_display.setReadOnly(True)

        self.scene = QGraphicsScene()

        self.track_manager = None

        self.signature = None

        self.selected_track = 0

        self.show()

    def load_file_button_clicker(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open MIDI file", MIDI_FILES_PATH, "MIDI files (*.mid);;")
        print(filename)
        if filename:
            self.read_midi(filename)

    def read_midi(self, filename):
        reader = MidiReader()
        self.track_manager = reader.read_file(filename)
        self.notes_quantity_display.setPlainText(str(self.track_manager.notes_quantity))
        self.setup_track_list()

    def setup_track_list(self):
        print("LIST LENGTH: " + str(self.track_manager.track_count))
        self.track_list.clear()
        for track_number in range(0, self.track_manager.track_count):
            item = QListWidgetItem("Track " + str(track_number + 1))
            self.track_list.addItem(item)
            #print("My item: " + self.track_list.item(track_number))
        #self.track_list.addItems(["Track " + str(track_number + 1) for track_number in range(0, len(self.list_of_signatures))])
        self.track_list.itemClicked.connect(self.track_list_selection_changed)

    def track_list_selection_changed(self, item):
        print("List selection changed")
        print(item.text()[-1:])
        self.selected_track = track_number = int(item.text()[-1:]) - 1
        self.track_manager.handle_selection(track_number)
        if(self.track_manager.is_track_selected(track_number) is True):
            item.setBackground(QColor('green'))
        else:
            item.setBackground(QColor('white'))

    def draw_signature_graphics_view(self):
        circle_of_fifths = CircleOfFifths(self.signature_graphics_view, self.scene)
        circle_of_fifths.draw()
        #CHECK IF THE TRACK CONTAINS ANY NOTES, IN OTHER CASE THIS OPERATION MAKES NO SENSE AND DIVIDES BY 0
        print("self.list_of_signatures[3]")
        #print(self.list_of_signatures[self.selected_track])
        signature_graphic = SignatureGraphic(signature_of_fifths=self.signature,
                                             #THIS IS ARBITRAL CHOICE, MECHANISM FOR TRACKS HANDLING NEEDED
                                             signature_graphics_view=self.signature_graphics_view, scene=self.scene)
        signature_graphic.draw_vector_per_note()
        signature_graphic.draw_cvsf()
        signature_graphic.draw_mdasf()
        signature_graphic.draw_major_minor_mode_axis()
        signature_graphic.draw_tonation_information(self.result_information)

    def save_results_button_clicker(self):
        pass

    def calculate_button_clicker(self):
        if self.notes_window_start.document().isEmpty() is False \
                and self.notes_window_end.document().isEmpty() is False:
            window_start = int(self.notes_window_start.toPlainText())
            window_end = int(self.notes_window_end.toPlainText())
            if window_end < window_start:
                print("Start of window must be before end of window !")
                return
            self.signature = self.track_manager.calculate_signature(window_start, window_end, SignatureModes.DURATION)
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
