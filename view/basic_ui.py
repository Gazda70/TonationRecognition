from PyQt5.QtWidgets import QMainWindow, QPushButton, QGraphicsScene, QGraphicsView, \
    QComboBox, QListWidget, QTextEdit, QListWidgetItem, QLabel, QMessageBox, QCheckBox, QRadioButton, QFileDialog
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QColor

from file_manager.file_manager import MidiReader, FileInfo
from utils.signature_drawing import CircleOfFifths, SignatureGraphic
from model.definitions import ALGORITHM_NAMES, SAMPLE_CALCULATION_MODES, TONAL_PROFILE_NAMES, MIDI_FILES_PATH, \
    MAIN_UI_PAGE, AlgorithmInfo, RHYTMIC_VALUES, Algorithm, Profile, WindowModes
from algorithms.algorithm_manager import AlgorithmManager


class UI_MainPage(QMainWindow):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 934)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.algorithm_type_dropdown = QtWidgets.QComboBox(self.centralwidget)
        self.algorithm_type_dropdown.setGeometry(QtCore.QRect(530, 60, 271, 31))
        self.algorithm_type_dropdown.setObjectName("algorithm_type_dropdown")
        self.tonal_profiles_type = QtWidgets.QComboBox(self.centralwidget)
        self.tonal_profiles_type.setGeometry(QtCore.QRect(1130, 60, 271, 31))
        self.tonal_profiles_type.setObjectName("tonal_profiles_type")
        self.load_files_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_files_button.setGeometry(QtCore.QRect(20, 60, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.load_files_button.setFont(font)
        self.load_files_button.setObjectName("load_files_button")
        self.save_results_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_results_button.setGeometry(QtCore.QRect(200, 60, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.save_results_button.setFont(font)
        self.save_results_button.setObjectName("save_results_button")
        self.signature_graphic_view = QtWidgets.QGraphicsView(self.centralwidget)
        self.signature_graphic_view.setGeometry(QtCore.QRect(800, 230, 751, 631))
        self.signature_graphic_view.setObjectName("signature_graphic_view")
        self.calculate_button = QtWidgets.QPushButton(self.centralwidget)
        self.calculate_button.setGeometry(QtCore.QRect(510, 780, 281, 81))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.calculate_button.setFont(font)
        self.calculate_button.setObjectName("calculate_button")
        self.sample_calculation_mode = QtWidgets.QComboBox(self.centralwidget)
        self.sample_calculation_mode.setGeometry(QtCore.QRect(830, 60, 271, 31))
        self.sample_calculation_mode.setObjectName("sample_calculation_mode")
        self.track_list_label = QtWidgets.QLabel(self.centralwidget)
        self.track_list_label.setGeometry(QtCore.QRect(240, 180, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.track_list_label.setFont(font)
        self.track_list_label.setObjectName("track_list_label")
        self.track_list = QtWidgets.QListWidget(self.centralwidget)
        self.track_list.setGeometry(QtCore.QRect(240, 220, 181, 192))
        self.track_list.setObjectName("track_list")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(800, 170, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.result_information = QtWidgets.QLabel(self.centralwidget)
        self.result_information.setGeometry(QtCore.QRect(960, 170, 431, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.result_information.setFont(font)
        self.result_information.setObjectName("result_information")
        self.min_rhytmic_value = QtWidgets.QComboBox(self.centralwidget)
        self.min_rhytmic_value.setGeometry(QtCore.QRect(400, 585, 281, 21))
        self.min_rhytmic_value.setObjectName("min_rhytmic_value")
        self.max_number_of_notes = QtWidgets.QTextEdit(self.centralwidget)
        self.max_number_of_notes.setGeometry(QtCore.QRect(400, 500, 231, 31))
        self.max_number_of_notes.setObjectName("max_number_of_notes")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(400, 450, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 540, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.number_of_units = QtWidgets.QTextEdit(self.centralwidget)
        self.number_of_units.setGeometry(QtCore.QRect(40, 575, 311, 31))
        self.number_of_units.setObjectName("number_of_units")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 540, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.show_main_axis_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.show_main_axis_checkbox.setGeometry(QtCore.QRect(550, 230, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.show_main_axis_checkbox.setFont(font)
        self.show_main_axis_checkbox.setObjectName("show_main_axis_checkbox")
        self.show_mode_axis_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.show_mode_axis_checkbox.setGeometry(QtCore.QRect(550, 280, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.show_mode_axis_checkbox.setFont(font)
        self.show_mode_axis_checkbox.setObjectName("show_mode_axis_checkbox")
        self.show_cvsf_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.show_cvsf_checkbox.setGeometry(QtCore.QRect(550, 330, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.show_cvsf_checkbox.setFont(font)
        self.show_cvsf_checkbox.setObjectName("show_cvsf_checkbox")
        self.show_signature_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.show_signature_checkbox.setGeometry(QtCore.QRect(550, 380, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.show_signature_checkbox.setFont(font)
        self.show_signature_checkbox.setObjectName("show_signature_checkbox")
        self.sample_from_start = QtWidgets.QRadioButton(self.centralwidget)
        self.sample_from_start.setGeometry(QtCore.QRect(30, 430, 251, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.sample_from_start.setFont(font)
        self.sample_from_start.setObjectName("sample_from_start")
        self.sample_from_end = QtWidgets.QRadioButton(self.centralwidget)
        self.sample_from_end.setGeometry(QtCore.QRect(30, 490, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.sample_from_end.setFont(font)
        self.sample_from_end.setObjectName("sample_from_end")
        self.file_list = QtWidgets.QListWidget(self.centralwidget)
        self.file_list.setGeometry(QtCore.QRect(30, 220, 181, 192))
        self.file_list.setObjectName("file_list")
        self.track_list_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.track_list_label_2.setGeometry(QtCore.QRect(30, 180, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.track_list_label_2.setFont(font)
        self.track_list_label_2.setObjectName("track_list_label_2")
        self.move_window_forward_button = QtWidgets.QPushButton(self.centralwidget)
        self.move_window_forward_button.setGeometry(QtCore.QRect(200, 700, 151, 41))
        self.move_window_forward_button.setObjectName("move_window_forward_button")
        self.move_window_units = QtWidgets.QTextEdit(self.centralwidget)
        self.move_window_units.setGeometry(QtCore.QRect(40, 660, 311, 31))
        self.move_window_units.setObjectName("move_window_units")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 620, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.move_window_backward_button = QtWidgets.QPushButton(self.centralwidget)
        self.move_window_backward_button.setGeometry(QtCore.QRect(40, 700, 151, 41))
        self.move_window_backward_button.setObjectName("move_window_backward_button")
        self.rhytmic_values_multiplier = QtWidgets.QTextEdit(self.centralwidget)
        self.rhytmic_values_multiplier.setGeometry(QtCore.QRect(400, 660, 281, 31))
        self.rhytmic_values_multiplier.setObjectName("rhytmic_values_multiplier")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(400, 620, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.load_files_button.setText(_translate("MainWindow", "Load files"))
        self.save_results_button.setText(_translate("MainWindow", "Save results"))
        self.calculate_button.setText(_translate("MainWindow", "Calculate"))
        self.track_list_label.setText(_translate("MainWindow", "Track list"))
        self.label_7.setText(_translate("MainWindow", "Tonality:"))
        self.result_information.setText(_translate("MainWindow", "unknown"))
        self.label_4.setText(_translate("MainWindow", "Max number of notes"))
        self.label.setText(_translate("MainWindow", "Select base rhytmic value"))
        self.label_5.setText(_translate("MainWindow", "Number of units in sample"))
        self.show_main_axis_checkbox.setText(_translate("MainWindow", "Show main axis"))
        self.show_mode_axis_checkbox.setText(_translate("MainWindow", "Show mode axis"))
        self.show_cvsf_checkbox.setText(_translate("MainWindow", "Show vector"))
        self.show_signature_checkbox.setText(_translate("MainWindow", "Show signature"))
        self.sample_from_start.setText(_translate("MainWindow", "Sample from start"))
        self.sample_from_end.setText(_translate("MainWindow", "Sample from end"))
        self.track_list_label_2.setText(_translate("MainWindow", "File list"))
        self.move_window_forward_button.setText(_translate("MainWindow", "Move window forward"))
        self.label_2.setText(_translate("MainWindow", "Units to move window"))
        self.move_window_backward_button.setText(_translate("MainWindow", "Move window backward"))
        self.label_3.setText(_translate("MainWindow", "Select multiplier"))
    def __init__(self):
        super(UI_MainPage, self).__init__()
        #uic.loadUi(MAIN_UI_PAGE, self)
        self.main_window = QMainWindow()
        self.setupUi(self.main_window)
        #self.load_file_button = self.findChild(QPushButton, "load_files_button")
        self.load_files_button.clicked.connect(self.load_file_button_clicker)

        # self.save_results_button = self.findChild(QPushButton, "save_results_button")
        self.save_results_button.clicked.connect(self.save_results_button_clicker)

        # self.algorithm_type_dropdown = self.findChild(QComboBox, "algorithm_type_dropdown")
        self.algorithm_type_dropdown.addItems(["Signature of fifths with major/minor axis", "Signature of fifths with tonal profiles"])

        # self.sample_calculation_mode = self.findChild(QComboBox, "sample_calculation_mode")
        self.sample_calculation_mode.addItems(SAMPLE_CALCULATION_MODES.keys())

        # self.tonal_profiles_type = self.findChild(QComboBox, "tonal_profiles_type")
        self.tonal_profiles_type.addItems(TONAL_PROFILE_NAMES.keys())

        # self.midi_channel_dropdown = self.findChild(QComboBox, "midi_channel_dropdown")

        # self.calculate_button = self.findChild(QPushButton, "calculate_button")
        self.calculate_button.clicked.connect(self.calculate_button_clicker)

        self.move_window_backward_button.clicked.connect(self.move_window_backward)

        self.move_window_forward_button.clicked.connect(self.move_window_forward)

        # self.signature_graphics_view = self.findChild(QGraphicsView, "signature_graphic_view")

        # self.track_list = self.findChild(QListWidget, "track_list")
        self.track_list.itemClicked.connect(self.track_list_selection_changed)

        # self.file_list = self.findChild(QListWidget, "file_list")
        self.file_list.itemActivated.connect(self.file_list_selection_changed)

        # self.sample_from_start = self.findChild(QRadioButton, "sample_from_start")
        self.sample_from_start.toggled.connect(self.check_if_sample_from_start)

        # self.sample_from_end = self.findChild(QRadioButton, "sample_from_end")
        self.sample_from_end.toggled.connect(self.check_if_sample_from_end)

        # self.result_information = self.findChild(QLabel, "result_information")

        # self.window_start_position = self.findChild(QTextEdit, "window_start_position")
        #
        # self.window_end_position = self.findChild(QTextEdit, "window_end_position")
        #
        # self.units_from_start = self.findChild(QTextEdit, "units_from_start")
        #
        # self.units_from_end = self.findChild(QTextEdit, "units_from_end")

        # self.number_of_units = self.findChild(QTextEdit, "number_of_units")

        # self.max_number_of_notes = self.findChild(QTextEdit, "max_number_of_notes")

        # self.min_rhytmic_value = self.findChild(QComboBox, "min_rhytmic_value")
        self.min_rhytmic_value.addItems(RHYTMIC_VALUES.keys())
        self.min_rhytmic_value.currentTextChanged.connect(self.set_base_rhytmic_value)

        # self.show_main_axis_checkbox = self.findChild(QCheckBox, "show_main_axis_checkbox")
        self.show_main_axis_checkbox.setChecked(True)
        self.show_main_axis_checkbox.stateChanged.connect(self.show_main_axis_state_changed)

        # self.show_mode_axis_checkbox = self.findChild(QCheckBox, "show_mode_axis_checkbox")
        self.show_mode_axis_checkbox.setChecked(True)
        self.show_mode_axis_checkbox.stateChanged.connect(self.show_mode_axis_state_changed)

        # self.show_cvsf_checkbox = self.findChild(QCheckBox, "show_cvsf_checkbox")
        self.show_cvsf_checkbox.setChecked(True)
        self.show_cvsf_checkbox.stateChanged.connect(self.show_cvsf_state_changed)

        # self.show_signature_checkbox = self.findChild(QCheckBox, "show_signature_checkbox")
        self.show_signature_checkbox.setChecked(True)
        self.show_signature_checkbox.stateChanged.connect(self.show_signature_state_changed)

        self.max_number_of_notes.setReadOnly(True)

        self.scene = None

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

        self.is_file_selected = False

        self.is_track_selected = False

        self.max_number_of_notes_to_check = 0

        self.window_calculation_mode = WindowModes.FROM_START

        self.global_track_length = 0

        self.filenames = []

        self.analysis_results = []

        self.files = []

        self.selected_file_number = 0

        self.window_start = 0

        self.window_end = 0

        self.rhytmic_values_multiplier.setText(str(1))

        self.main_window.show()
        #self.show()

    def move_window_backward(self):
        if not self.move_window_units.toPlainText().isdigit():
            QMessageBox.warning(self.scene, "Error", "Move offset must be an positive integer !")
        elif self.move_window_units.document().isEmpty() is True:
            QMessageBox.warning(self.scene, "Error", "Select move offset !")
        else:
            move_window_units = int(self.move_window_units.toPlainText())
            if self.window_start - move_window_units < 0:
                QMessageBox.warning(self.scene, "Error", "Move window out of range !")
                return
            else:
                self.window_start -= move_window_units
                self.window_end -= move_window_units

    def move_window_forward(self):
        if not self.move_window_units.toPlainText().isdigit():
            QMessageBox.warning(self.scene, "Error", "Move offset must be an positive integer !")
        elif self.move_window_units.document().isEmpty() is True:
            QMessageBox.warning(self.scene, "Error", "Select move offset !")
        else:
            move_window_units = int(self.move_window_units.toPlainText())
            if self.window_start + move_window_units > self.max_number_of_notes_to_check:
                QMessageBox.warning(self.scene, "Error", "Move window out of range !")
                return
            else:
                self.window_start += move_window_units
                self.window_end += move_window_units

    def check_if_sample_from_start(self):
        if self.sample_from_start.isChecked():
            self.window_calculation_mode = WindowModes.FROM_START

    def check_if_sample_from_end(self):
        if self.sample_from_end.isChecked():
            self.window_calculation_mode = WindowModes.FROM_END

    def load_file_button_clicker(self):
        self.filenames, _ = QFileDialog.getOpenFileNames(self, "Open MIDI file", MIDI_FILES_PATH, "MIDI files (*.mid);;")
        file_number = 0
        if len(self.filenames) > 0:
            self.track_list.clear()
            self.is_file = True
            self.files = []
            for filename in self.filenames:
                reader = MidiReader()
                self.read_midi(filename, reader, file_number)
                file_number += 1
            self.setup_file_list()

    def read_midi(self, filename, reader, file_number):
        file, track_manager = reader.read_file(filename)
        self.files.append(FileInfo(file, track_manager, False, file_number))

    def setup_track_list(self):
        self.track_list.clear()
        for track_number in range(0, self.files[self.selected_file_number].track_manager.track_count):
            item = QListWidgetItem("Track " + str(track_number + 1))
            self.track_list.addItem(item)


    def setup_file_list(self):
        self.analysis_results.clear()
        self.file_list.clear()
        for filename in self.filenames:
            item = QListWidgetItem(filename)
            self.file_list.addItem(item)
        self.file_list.itemClicked.connect(self.file_list_selection_changed)


    def file_list_selection_changed(self, item):
        self.is_file_selected = True
        self.selected_file_number = next(file_info for file_info in self.files if file_info.file.filename == item.text()).file_number
        item.setBackground(QColor('green'))
        for index in range(self.file_list.count()):
            if self.file_list.item(index).text() != item.text():
                self.file_list.item(index).setBackground(QColor('white'))
        self.max_number_of_notes_to_check = self.files[self.selected_file_number]\
            .track_manager.calculate_base_rhytmic_value_multiplicity(RHYTMIC_VALUES[self.min_rhytmic_value.currentText()])
        self.max_number_of_notes.setText(str(self.max_number_of_notes_to_check))
        self.global_track_length = self.files[self.selected_file_number].track_manager.get_operable_range_of_all_tracks()
        self.setup_track_list()


    def track_list_selection_changed(self, item):
        self.is_track_selected = True
        self.selected_track = track_number = int(item.text()[-1:]) - 1
        self.files[self.selected_file_number].track_manager.handle_selection(track_number)
        if (self.files[self.selected_file_number].track_manager.is_track_selected(track_number) is True):
            item.setBackground(QColor('green'))
        else:
            item.setBackground(QColor('white'))

    def set_base_rhytmic_value(self, note_resolution):
        if self.is_file == False:
            QMessageBox.warning(self.scene, "Error", "Select file !")
        else:
            self.max_number_of_notes_to_check = self.files[self.selected_file_number].track_manager.calculate_base_rhytmic_value_multiplicity(RHYTMIC_VALUES[self.min_rhytmic_value.currentText()])
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
            circle_of_fifths = CircleOfFifths(self.signature_graphic_view, self.scene)
            circle_of_fifths.draw()
            signature_graphic = SignatureGraphic(signature_of_fifths=signature,
                                                 signature_graphics_view=self.signature_graphic_view, scene=self.scene)
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
        reader = MidiReader()
        reader.write_results(self, self.analysis_results)
        self.analysis_results.clear()


    def remember_results(self, algorithm_info, window_start, window_end, base_rhythmic_value, ks_results, as_results, t_results):
        self.analysis_results.append({"FILENAME":self.files[self.selected_file_number].file.filename,
                                      "SELECTED_TRACKS":self.files[self.selected_file_number].track_manager.get_selected_tracks_numbers(),
                                      "WINDOW_START":window_start,
                                      "WINDOW_END":window_end,
                                      "BASE_RHYTHMIC_VALUE":base_rhythmic_value,
                                      "ALGORITHM_INFO":algorithm_info,
                                      "KS_RESULTS":ks_results,
                                      "AS_RESULTS":as_results,
                                      "T_RESULTS":t_results})

    def calculate_button_clicker(self):
        if self.number_of_units.document().isEmpty():
            QMessageBox.warning(self.scene, "Error", "Select window !")
            return
        if not self.number_of_units.toPlainText().isdigit():
            QMessageBox.warning(self.scene, "Error", "Window size be an positive integer !")
            return
        number_of_units = int(self.number_of_units.toPlainText())
        if self.is_file_selected == False:
            QMessageBox.warning(self.scene, "Error", "Select file !")
        elif self.is_track_selected == False:
            QMessageBox.warning(self.scene, "Error", "Select track !")
        elif self.max_number_of_notes.document().isEmpty() is True:
            QMessageBox.warning(self.scene, "Error", "Select time window !")
        elif number_of_units < 0 or number_of_units > self.max_number_of_notes_to_check:
            QMessageBox.warning(self.scene, "Error", "Window must match constraints !")
        else:
            if not self.rhytmic_values_multiplier.toPlainText().isdigit():
                QMessageBox.warning(self.scene, "Error", "Multiplier must be an positive integer !")
                return
            multiplier = int(self.rhytmic_values_multiplier.toPlainText())
            if multiplier > self.max_number_of_notes_to_check:
                QMessageBox.warning(self.scene, "Error", "Bad multiplier !")
                return
            self.window_start = 0
            self.window_end = 0
            if self.window_calculation_mode == WindowModes.FROM_START:
                if number_of_units * multiplier > self.max_number_of_notes_to_check:
                    QMessageBox.warning(self.scene, "Error", "Bad multiplier !")
                    return
                self.window_start = 0
                self.window_end = number_of_units * multiplier
            elif self.window_calculation_mode == WindowModes.FROM_END:
                if (self.max_number_of_notes_to_check - number_of_units)  * multiplier > self.max_number_of_notes_to_check:
                    QMessageBox.warning(self.scene, "Error", "Bad multiplier !")
                    return
                self.window_start = (self.max_number_of_notes_to_check - number_of_units)  * multiplier
                self.window_end = self.max_number_of_notes_to_check
            algorithm_info = AlgorithmInfo(
                algorithm_type=ALGORITHM_NAMES[self.algorithm_type_dropdown.currentText()],
                sample_calculation_mode=SAMPLE_CALCULATION_MODES[self.sample_calculation_mode.currentText()],
                profile=TONAL_PROFILE_NAMES[self.tonal_profiles_type.currentText()])
            result_information, self.signature = self.algorithm_manager.execute_algorithm(algorithm_info,
                                                                                     self.files[self.selected_file_number].track_manager.calculate_sample_vector(
                                                                                         self.window_start, self.window_end,
                                                                                         SAMPLE_CALCULATION_MODES[
                                                                                             self.sample_calculation_mode.currentText()], self.min_rhytmic_value.currentText()))


            if self.signature.is_empty() == True:
                QMessageBox.warning(self.scene, "Error", "Selected sample doesn't contain any pitches !")
            else:                        
                self.ks_results, _ = self.algorithm_manager.execute_algorithm(AlgorithmInfo(
                    algorithm_type=Algorithm.CLASSIC_TONAL_PROFILES,
                    sample_calculation_mode=SAMPLE_CALCULATION_MODES[self.sample_calculation_mode.currentText()],
                    profile=Profile.KS),
                                                                                         self.files[self.selected_file_number].track_manager.calculate_sample_vector(
                                                                                             self.window_start, self.window_end,
                                                                                             SAMPLE_CALCULATION_MODES[
                                                                                                 self.sample_calculation_mode.currentText()],
                                                                                             self.min_rhytmic_value.currentText()))

                self.as_results, _ = self.algorithm_manager.execute_algorithm(AlgorithmInfo(
                    algorithm_type=Algorithm.CLASSIC_TONAL_PROFILES,
                    sample_calculation_mode=SAMPLE_CALCULATION_MODES[self.sample_calculation_mode.currentText()],
                    profile=Profile.AS),
                                                                                         self.files[self.selected_file_number].track_manager.calculate_sample_vector(
                                                                                             self.window_start, self.window_end,
                                                                                             SAMPLE_CALCULATION_MODES[
                                                                                                 self.sample_calculation_mode.currentText()],
                                                                                             self.min_rhytmic_value.currentText()))

                self.t_results, _ = self.algorithm_manager.execute_algorithm(AlgorithmInfo(
                    algorithm_type=Algorithm.CLASSIC_TONAL_PROFILES,
                    sample_calculation_mode=SAMPLE_CALCULATION_MODES[self.sample_calculation_mode.currentText()],
                    profile=Profile.T),
                                                                                         self.files[self.selected_file_number].track_manager.calculate_sample_vector(
                                                                                             self.window_start, self.window_end,
                                                                                             SAMPLE_CALCULATION_MODES[
                                                                                                 self.sample_calculation_mode.currentText()],
                                                                                             self.min_rhytmic_value.currentText()))
                self.result_information.setText(result_information)
                self.draw_signature_graphics_view(self.signature, self.ks_results, self.as_results, self.t_results)
                self.remember_results(algorithm_info, self.window_start, self.window_end, self.min_rhytmic_value.currentText(), self.ks_results,
                                 self.as_results, self.t_results)



'''
Bug z nie wyświetlaniem tonacji dla wartości przy końcu zakresu, przy zakresie określonym przez wyświetlaną wartość
jest powodowany złym obliczeniem zakresu - pod koniec już nie ma nut.
Występuje dla niewielkich wartości rytmicznych - poniżej ósemki.
'''
