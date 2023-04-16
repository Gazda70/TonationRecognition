import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QGraphicsScene, QGraphicsView, \
    QComboBox, QListWidget, QTextEdit, QListWidgetItem, QLabel, QMessageBox
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QColor
from file_manager.file_manager import MidiReader
from signature_drawing import CircleOfFifths, SignatureGraphic
from model.definitions import SampleMode, ALGORITHM_NAMES, SAMPLE_CALCULATION_MODES, TONAL_PROFILE_NAMES, MIDI_FILES_PATH, MAIN_UI_PAGE



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
        self.algorithm_type_dropdown.addItems(ALGORITHM_NAMES)

        self.sample_calculation_dropdown = self.findChild(QComboBox, "sample_calculation_mode")
        self.sample_calculation_dropdown.addItems(SAMPLE_CALCULATION_MODES)

        self.tonal_profiles_dropdown = self.findChild(QComboBox, "tonal_profiles_type")
        self.tonal_profiles_dropdown.addItems(TONAL_PROFILE_NAMES)

        self.midi_channel_dropdown = self.findChild(QComboBox, "midi_channel_dropdown")

        self.calculate_signature_button = self.findChild(QPushButton, "calculate_button")
        self.calculate_signature_button.clicked.connect(self.calculate_button_clicker)

        self.signature_graphics_view = self.findChild(QGraphicsView, "signature_graphic_view")

        self.track_list = self.findChild(QListWidget, "track_list")

        self.result_information = self.findChild(QLabel, "result_information")

        self.notes_window_start = self.findChild(QTextEdit, "notes_window_start")

        self.notes_window_end = self.findChild(QTextEdit, "notes_window_end")

        self.scene = None

        self.track_manager = None

        self.signature = None

        self.selected_track = 0

        self.is_file = False

        self.show()

    def load_file_button_clicker(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open MIDI file", MIDI_FILES_PATH, "MIDI files (*.mid);;")
        print(filename)
        if filename:
            self.read_midi(filename)

    def read_midi(self, filename):
        reader = MidiReader()
        self.track_manager = reader.read_file(filename)
        self.setup_track_list()
        self.is_file = True

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
        self.scene = QGraphicsScene()
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
        if self.is_file == False:
            QMessageBox.warning(self.scene, "Error", "Select file !")
        elif self.notes_window_start.document().isEmpty() is True \
                or self.notes_window_end.document().isEmpty() is True:
            QMessageBox.warning(self.scene, "Error", "Select time window !")
        else:
            window_start = int(self.notes_window_start.toPlainText())
            window_end = int(self.notes_window_end.toPlainText())
            if window_end <= window_start:
                QMessageBox.warning(self.scene, "Error", "Start of window must be before end of window !")
            else:
                if self.sample_calculation_dropdown.currentText() == SAMPLE_CALCULATION_MODES[0]:
                    self.signature = self.track_manager.calculate_signature(window_start, window_end, SampleMode.QUANTITY)
                elif self.sample_calculation_dropdown.currentText() == SAMPLE_CALCULATION_MODES[1]:
                    self.signature = self.track_manager.calculate_signature(window_start, window_end, SampleMode.DURATION)
                self.draw_signature_graphics_view()


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
main_ui_page = UI_MainPage()
widget.addWidget(main_ui_page)
w = 1500
h = 1100
widget.resize(w, h)
widget.show()
app.exec_()
