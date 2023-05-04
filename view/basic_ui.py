import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QGraphicsScene, QGraphicsView, \
    QComboBox, QListWidget, QTextEdit, QListWidgetItem, QLabel, QMessageBox, QCheckBox
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QColor
from file_manager.file_manager import MidiReader
from signature_drawing import CircleOfFifths, SignatureGraphic
from model.definitions import ALGORITHM_NAMES, SAMPLE_CALCULATION_MODES, TONAL_PROFILE_NAMES, MIDI_FILES_PATH, \
    MAIN_UI_PAGE, AlgorithmInfo, RHYTMIC_VALUES, Algorithm, Profile
from algorithms.algorithm_manager import AlgorithmManager


class UI_MainPage(QMainWindow):
    def __init__(self):
        super(UI_MainPage, self).__init__()

        uic.loadUi(MAIN_UI_PAGE, self)
        self.load_file_button = self.findChild(QPushButton, "load_files_button")
        self.load_file_button.clicked.connect(self.load_file_button_clicker)

        self.save_results_button = self.findChild(QPushButton, "save_results_button")
        self.save_results_button.clicked.connect(self.save_results_button_clicker)

        self.algorithm_type_dropdown = self.findChild(QComboBox, "algorithm_type_dropdown")
        self.algorithm_type_dropdown.addItems(ALGORITHM_NAMES.keys())

        self.sample_calculation_dropdown = self.findChild(QComboBox, "sample_calculation_mode")
        self.sample_calculation_dropdown.addItems(SAMPLE_CALCULATION_MODES.keys())

        self.tonal_profiles_dropdown = self.findChild(QComboBox, "tonal_profiles_type")
        self.tonal_profiles_dropdown.addItems(TONAL_PROFILE_NAMES.keys())

        self.midi_channel_dropdown = self.findChild(QComboBox, "midi_channel_dropdown")

        self.calculate_signature_button = self.findChild(QPushButton, "calculate_button")
        self.calculate_signature_button.clicked.connect(self.calculate_button_clicker)

        self.signature_graphics_view = self.findChild(QGraphicsView, "signature_graphic_view")

        self.track_list = self.findChild(QListWidget, "track_list")

        self.result_information = self.findChild(QLabel, "result_information")

        self.window_start_position = self.findChild(QTextEdit, "window_start_position")

        self.window_end_position = self.findChild(QTextEdit, "window_end_position")

        self.units_from_start = self.findChild(QTextEdit, "units_from_start")

        self.units_from_end = self.findChild(QTextEdit, "units_from_end")

        self.max_number_of_notes = self.findChild(QTextEdit, "max_number_of_notes")

        self.min_rhytmic_value = self.findChild(QComboBox, "min_rhytmic_value")
        self.min_rhytmic_value.addItems(RHYTMIC_VALUES.keys())
        self.min_rhytmic_value.currentTextChanged.connect(self.set_base_rhytmic_value)

        self.show_main_axis_checkbox = self.findChild(QCheckBox, "show_main_axis_checkbox")
        self.show_main_axis_checkbox.setChecked(True)
        self.show_main_axis_checkbox.stateChanged.connect(self.show_main_axis_state_changed)

        self.show_mode_axis_checkbox = self.findChild(QCheckBox, "show_mode_axis_checkbox")
        self.show_mode_axis_checkbox.setChecked(True)
        self.show_mode_axis_checkbox.stateChanged.connect(self.show_mode_axis_state_changed)

        self.show_cvsf_checkbox = self.findChild(QCheckBox, "show_cvsf_checkbox")
        self.show_cvsf_checkbox.setChecked(True)
        self.show_cvsf_checkbox.stateChanged.connect(self.show_cvsf_state_changed)

        self.show_signature_checkbox = self.findChild(QCheckBox, "show_signature_checkbox")
        self.show_signature_checkbox.setChecked(True)
        self.show_signature_checkbox.stateChanged.connect(self.show_signature_state_changed)

        self.scene = None

        self.track_manager = None

        self.algorithm_manager = AlgorithmManager()

        self.signature = None

        self.ks_results = None

        self.as_results = None

        self.t_results = None

        self.draw_mdasf = True

        self.draw_mode = True

        self.draw_cvsf = True

        self.draw_signature = True

        self.selected_track = 0

        self.is_file = False

        self.max_number_of_notes_to_check = 0

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
        self.max_number_of_notes_to_check = self.track_manager.calculate_base_rhytmic_value_multiplicity(RHYTMIC_VALUES[self.min_rhytmic_value.currentText()])
        self.max_number_of_notes.setText(str(self.max_number_of_notes_to_check))
        self.is_file = True

    def setup_track_list(self):
        self.track_list.clear()
        for track_number in range(0, self.track_manager.track_count):
            item = QListWidgetItem("Track " + str(track_number + 1))
            self.track_list.addItem(item)
        self.track_list.itemClicked.connect(self.track_list_selection_changed)

    def track_list_selection_changed(self, item):
        self.selected_track = track_number = int(item.text()[-1:]) - 1
        self.track_manager.handle_selection(track_number)
        if (self.track_manager.is_track_selected(track_number) is True):
            item.setBackground(QColor('green'))
        else:
            item.setBackground(QColor('white'))

    def set_base_rhytmic_value(self, note_resolution):
        if self.is_file == False:
            QMessageBox.warning(self.scene, "Error", "Select file !")
        else:
            self.max_number_of_notes_to_check = self.track_manager.calculate_base_rhytmic_value_multiplicity(
                RHYTMIC_VALUES[self.min_rhytmic_value.currentText()])
            self.max_number_of_notes.setText(str(self.max_number_of_notes_to_check))

    def show_main_axis_state_changed(self, item):
        if self.show_main_axis_checkbox.isChecked():
            self.draw_mdasf = True
        else:
            self.draw_mdasf = False
        self.draw_signature_graphics_view(self.signature, self.ks_results, self.as_results, self.t_results)
    def show_mode_axis_state_changed(self, item):
        if self.show_mode_axis_checkbox.isChecked():
            self.draw_mode = True
        else:
            self.draw_mode = False
        self.draw_signature_graphics_view(self.signature, self.ks_results, self.as_results, self.t_results)

    def show_cvsf_state_changed(self, item):
        if self.show_cvsf_checkbox.isChecked():
            self.draw_cvsf = True
        else:
            self.draw_cvsf = False
        self.draw_signature_graphics_view(self.signature, self.ks_results, self.as_results, self.t_results)

    def show_signature_state_changed(self, item):
        if self.show_signature_checkbox.isChecked():
            self.draw_signature = True
        else:
            self.draw_signature = False
        self.draw_signature_graphics_view(self.signature, self.ks_results, self.as_results, self.t_results)

    def draw_signature_graphics_view(self, signature, ks_results, as_results, t_results):
        if self.signature != None and self.ks_results != None and self.as_results != None and self.t_results != None:
            self.scene = QGraphicsScene()
            circle_of_fifths = CircleOfFifths(self.signature_graphics_view, self.scene)
            circle_of_fifths.draw()
            signature_graphic = SignatureGraphic(signature_of_fifths=signature,
                                                 signature_graphics_view=self.signature_graphics_view, scene=self.scene)
            if self.draw_signature:
                signature_graphic.draw_vector_per_note()
            if self.draw_cvsf:
                signature_graphic.draw_cvsf()
            if self.draw_mdasf:
                signature_graphic.draw_mdasf()
            if self.draw_mode:
                signature_graphic.draw_major_minor_mode_axis()
            signature_graphic.draw_tonal_profiles_results(ks_results, as_results, t_results)

    def save_results_button_clicker(self):
        pass

    def calculate_button_clicker(self):
        if self.is_file == False:
            QMessageBox.warning(self.scene, "Error", "Select file !")
        elif self.window_start_position.document().isEmpty() is True \
                or self.window_end_position.document().isEmpty() is True:
            QMessageBox.warning(self.scene, "Error", "Select time window !")
        else:
            window_start = int(self.window_start_position.toPlainText())
            window_end = int(self.window_end_position.toPlainText())
            if window_start < 0 or window_end > self.max_number_of_notes_to_check:
                QMessageBox.warning(self.scene, "Error", "Window must match constraints !")
            elif window_end <= window_start:
                QMessageBox.warning(self.scene, "Error", "Start of window must be before end of window !")
            else:
                algorithm_info = AlgorithmInfo(
                    algorithm_type=ALGORITHM_NAMES[self.algorithm_type_dropdown.currentText()],
                    sample_calculation_mode=SAMPLE_CALCULATION_MODES[self.sample_calculation_dropdown.currentText()],
                    profile=TONAL_PROFILE_NAMES[self.tonal_profiles_dropdown.currentText()])
                result_information, self.signature = self.algorithm_manager.execute_algorithm(algorithm_info,
                                                                                         self.track_manager.calculate_sample_vector(
                                                                                             window_start, window_end,
                                                                                             SAMPLE_CALCULATION_MODES[
                                                                                                 self.sample_calculation_dropdown.currentText()], self.min_rhytmic_value.currentText()))

                self.ks_results, _ = self.algorithm_manager.execute_algorithm(AlgorithmInfo(
                    algorithm_type=Algorithm.CLASSIC_TONAL_PROFILES,
                    sample_calculation_mode=SAMPLE_CALCULATION_MODES[self.sample_calculation_dropdown.currentText()],
                    profile=Profile.KS),
                                                                                         self.track_manager.calculate_sample_vector(
                                                                                             window_start, window_end,
                                                                                             SAMPLE_CALCULATION_MODES[
                                                                                                 self.sample_calculation_dropdown.currentText()],
                                                                                             self.min_rhytmic_value.currentText()))

                self.as_results, _ = self.algorithm_manager.execute_algorithm(AlgorithmInfo(
                    algorithm_type=Algorithm.CLASSIC_TONAL_PROFILES,
                    sample_calculation_mode=SAMPLE_CALCULATION_MODES[self.sample_calculation_dropdown.currentText()],
                    profile=Profile.AS),
                                                                                         self.track_manager.calculate_sample_vector(
                                                                                             window_start, window_end,
                                                                                             SAMPLE_CALCULATION_MODES[
                                                                                                 self.sample_calculation_dropdown.currentText()],
                                                                                             self.min_rhytmic_value.currentText()))

                self.t_results, _ = self.algorithm_manager.execute_algorithm(AlgorithmInfo(
                    algorithm_type=Algorithm.CLASSIC_TONAL_PROFILES,
                    sample_calculation_mode=SAMPLE_CALCULATION_MODES[self.sample_calculation_dropdown.currentText()],
                    profile=Profile.T),
                                                                                         self.track_manager.calculate_sample_vector(
                                                                                             window_start, window_end,
                                                                                             SAMPLE_CALCULATION_MODES[
                                                                                                 self.sample_calculation_dropdown.currentText()],
                                                                                             self.min_rhytmic_value.currentText()))
                self.result_information.setText(result_information)
                self.draw_signature_graphics_view(self.signature, self.ks_results, self.as_results, self.t_results)


if ( __name__ == '__main__' ):
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    main_ui_page = UI_MainPage()
    widget.addWidget(main_ui_page)
    w = 1800
    h = 900
    widget.resize(w, h)
    widget.show()
    app.exec_()
