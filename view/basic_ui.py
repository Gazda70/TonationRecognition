from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QListWidgetItem, QMessageBox, QFileDialog, QProgressDialog
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QColor

from file_manager.file_manager import MidiReader, FileInfo
from utils.mappings import create_main_axis_string
from utils.signature_drawing import CircleOfFifths, SignatureGraphic
from model.definitions import ALGORITHM_NAMES, SAMPLE_CALCULATION_MODES, TONAL_PROFILE_NAMES, MIDI_FILES_PATH, \
    AlgorithmInfo, RHYTHMIC_VALUES, Algorithm, Profile, NoteVectorDirection
from algorithms.algorithm_manager import AlgorithmManager


class UI_MainPage(QMainWindow):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1653, 934)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.algorithm_type_dropdown = QtWidgets.QComboBox(self.centralwidget)
        self.algorithm_type_dropdown.setGeometry(QtCore.QRect(490, 60, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.algorithm_type_dropdown.setFont(font)
        self.algorithm_type_dropdown.setObjectName("algorithm_type_dropdown")
        self.tonal_profiles_type = QtWidgets.QComboBox(self.centralwidget)
        self.tonal_profiles_type.setGeometry(QtCore.QRect(1190, 60, 361, 51))
        self.tonal_profiles_type.setMinimumSize(QtCore.QSize(271, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.tonal_profiles_type.setFont(font)
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
        self.calculate_button.setGeometry(QtCore.QRect(560, 440, 181, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.calculate_button.setFont(font)
        self.calculate_button.setObjectName("calculate_button")
        self.sample_calculation_mode = QtWidgets.QComboBox(self.centralwidget)
        self.sample_calculation_mode.setGeometry(QtCore.QRect(840, 60, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.sample_calculation_mode.setFont(font)
        self.sample_calculation_mode.setObjectName("sample_calculation_mode")
        self.track_list_label = QtWidgets.QLabel(self.centralwidget)
        self.track_list_label.setGeometry(QtCore.QRect(240, 180, 181, 31))
        self.track_list_label.setMinimumSize(QtCore.QSize(121, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.track_list_label.setFont(font)
        self.track_list_label.setObjectName("track_list_label")
        self.track_list = QtWidgets.QListWidget(self.centralwidget)
        self.track_list.setGeometry(QtCore.QRect(240, 220, 181, 192))
        self.track_list.setObjectName("track_list")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(800, 170, 301, 51))
        self.label_7.setMinimumSize(QtCore.QSize(301, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.result_information = QtWidgets.QLabel(self.centralwidget)
        self.result_information.setGeometry(QtCore.QRect(1000, 170, 431, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.result_information.sizePolicy().hasHeightForWidth())
        self.result_information.setSizePolicy(sizePolicy)
        self.result_information.setMinimumSize(QtCore.QSize(431, 51))
        self.result_information.setMaximumSize(QtCore.QSize(0, 0))
        self.result_information.setSizeIncrement(QtCore.QSize(0, 0))
        self.result_information.setBaseSize(QtCore.QSize(431, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.result_information.setFont(font)
        self.result_information.setObjectName("result_information")
        self.min_rhythmic_value = QtWidgets.QComboBox(self.centralwidget)
        self.min_rhythmic_value.setGeometry(QtCore.QRect(520, 540, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.min_rhythmic_value.setFont(font)
        self.min_rhythmic_value.setObjectName("min_rhythmic_value")
        self.max_number_of_notes = QtWidgets.QTextEdit(self.centralwidget)
        self.max_number_of_notes.setGeometry(QtCore.QRect(280, 460, 231, 31))
        self.max_number_of_notes.setObjectName("max_number_of_notes")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(280, 420, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(520, 500, 281, 41))
        self.label.setMinimumSize(QtCore.QSize(221, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.number_of_units = QtWidgets.QTextEdit(self.centralwidget)
        self.number_of_units.setGeometry(QtCore.QRect(30, 460, 231, 31))
        self.number_of_units.setObjectName("number_of_units")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 420, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.show_main_axis_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.show_main_axis_checkbox.setGeometry(QtCore.QRect(530, 230, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.show_main_axis_checkbox.setFont(font)
        self.show_main_axis_checkbox.setObjectName("show_main_axis_checkbox")
        self.show_mode_axis_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.show_mode_axis_checkbox.setGeometry(QtCore.QRect(530, 280, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.show_mode_axis_checkbox.setFont(font)
        self.show_mode_axis_checkbox.setObjectName("show_mode_axis_checkbox")
        self.show_cvsf_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.show_cvsf_checkbox.setGeometry(QtCore.QRect(530, 330, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.show_cvsf_checkbox.setFont(font)
        self.show_cvsf_checkbox.setObjectName("show_cvsf_checkbox")
        self.show_signature_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.show_signature_checkbox.setGeometry(QtCore.QRect(530, 380, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.show_signature_checkbox.setFont(font)
        self.show_signature_checkbox.setObjectName("show_signature_checkbox")
        self.file_list = QtWidgets.QListWidget(self.centralwidget)
        self.file_list.setGeometry(QtCore.QRect(30, 220, 181, 192))
        self.file_list.setObjectName("file_list")
        self.track_list_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.track_list_label_2.setGeometry(QtCore.QRect(30, 180, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.track_list_label_2.setFont(font)
        self.track_list_label_2.setObjectName("track_list_label_2")
        self.move_window_forward_button = QtWidgets.QPushButton(self.centralwidget)
        self.move_window_forward_button.setGeometry(QtCore.QRect(180, 810, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.move_window_forward_button.setFont(font)
        self.move_window_forward_button.setObjectName("move_window_forward_button")
        self.move_window_offset = QtWidgets.QTextEdit(self.centralwidget)
        self.move_window_offset.setGeometry(QtCore.QRect(20, 770, 311, 31))
        self.move_window_offset.setObjectName("move_window_offset")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 730, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.move_window_backward_button = QtWidgets.QPushButton(self.centralwidget)
        self.move_window_backward_button.setGeometry(QtCore.QRect(20, 810, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.move_window_backward_button.setFont(font)
        self.move_window_backward_button.setObjectName("move_window_backward_button")
        self.expand_window_button = QtWidgets.QPushButton(self.centralwidget)
        self.expand_window_button.setGeometry(QtCore.QRect(510, 810, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.expand_window_button.setFont(font)
        self.expand_window_button.setObjectName("expand_window_button")
        self.reduce_window_button = QtWidgets.QPushButton(self.centralwidget)
        self.reduce_window_button.setGeometry(QtCore.QRect(350, 810, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.reduce_window_button.setFont(font)
        self.reduce_window_button.setObjectName("reduce_window_button")
        self.expand_window_offset = QtWidgets.QTextEdit(self.centralwidget)
        self.expand_window_offset.setGeometry(QtCore.QRect(350, 770, 311, 31))
        self.expand_window_offset.setObjectName("expand_window_offset")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(350, 730, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.window_start = QtWidgets.QTextEdit(self.centralwidget)
        self.window_start.setGeometry(QtCore.QRect(20, 690, 191, 31))
        self.window_start.setObjectName("window_start")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 650, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(350, 650, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.window_end = QtWidgets.QTextEdit(self.centralwidget)
        self.window_end.setGeometry(QtCore.QRect(350, 690, 191, 31))
        self.window_end.setObjectName("window_end")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1653, 26))
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
        self.load_files_button.setText(_translate("MainWindow", "Load"))
        self.save_results_button.setText(_translate("MainWindow", "Save"))
        self.calculate_button.setText(_translate("MainWindow", "Calculate"))
        self.track_list_label.setText(_translate("MainWindow", "Track list"))
        self.label_7.setText(_translate("MainWindow", "Tonality:"))
        self.result_information.setText(_translate("MainWindow", "unknown"))
        self.label_4.setText(_translate("MainWindow", "Track length"))
        self.label.setText(_translate("MainWindow", "Base rhythmic value"))
        self.label_5.setText(_translate("MainWindow", "Sample"))
        self.show_main_axis_checkbox.setText(_translate("MainWindow", "Show main axis"))
        self.show_mode_axis_checkbox.setText(_translate("MainWindow", "Show mode axis"))
        self.show_cvsf_checkbox.setText(_translate("MainWindow", "Show vector"))
        self.show_signature_checkbox.setText(_translate("MainWindow", "Show signature"))
        self.track_list_label_2.setText(_translate("MainWindow", "File list"))
        self.move_window_forward_button.setText(_translate("MainWindow", "+"))
        self.label_2.setText(_translate("MainWindow", "Move window offset"))
        self.move_window_backward_button.setText(_translate("MainWindow", "-"))
        self.expand_window_button.setText(_translate("MainWindow", "+"))
        self.reduce_window_button.setText(_translate("MainWindow", "-"))
        self.label_6.setText(_translate("MainWindow", "Expand window"))
        self.label_3.setText(_translate("MainWindow", "Window start"))
        self.label_8.setText(_translate("MainWindow", "Window end"))
    def __init__(self):
        super(UI_MainPage, self).__init__()
        self.main_window = QMainWindow()
        self.setupUi(self.main_window)
        self.load_files_button.clicked.connect(self.load_file_button_clicker)

        self.save_results_button.clicked.connect(self.save_results_button_clicker)

        self.algorithm_type_dropdown.addItems(["Major/minor axis", "Tonal profiles"])

        self.sample_calculation_mode.addItems(SAMPLE_CALCULATION_MODES.keys())

        self.tonal_profiles_type.addItems(TONAL_PROFILE_NAMES.keys())

        self.calculate_button.clicked.connect(self.calculate_button_clicker)

        self.move_window_backward_button.clicked.connect(self.move_window_backward)

        self.move_window_forward_button.clicked.connect(self.move_window_forward)

        self.track_list.itemClicked.connect(self.track_list_selection_changed)

        self.file_list.itemActivated.connect(self.file_list_selection_changed)

        self.min_rhythmic_value.addItems(RHYTHMIC_VALUES.keys())

        self.show_main_axis_checkbox.setChecked(True)
        self.show_main_axis_checkbox.stateChanged.connect(self.show_main_axis_state_changed)

        self.show_mode_axis_checkbox.setChecked(True)
        self.show_mode_axis_checkbox.stateChanged.connect(self.show_mode_axis_state_changed)

        self.show_cvsf_checkbox.setChecked(True)
        self.show_cvsf_checkbox.stateChanged.connect(self.show_cvsf_state_changed)

        self.show_signature_checkbox.setChecked(True)
        self.show_signature_checkbox.stateChanged.connect(self.show_signature_state_changed)

        self.expand_window_button.clicked.connect(self.expand_window)
        self.reduce_window_button.clicked.connect(self.reduce_window)

        self.number_of_units.setText(str(1))
        self.move_window_offset.setText(str(1))
        self.expand_window_offset.setText(str(1))

        self.max_number_of_notes.setReadOnly(True)

        self.window_start.setReadOnly(True)

        self.window_end.setReadOnly(True)

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

        self.global_track_length = 0

        self.filenames = []

        self.analysis_results = []

        self.moving_window_analysis_result = []

        self.expanding_window_analysis_result = []

        self.moving_window_index = 0

        self.expanding_window_index = 0

        self.files = []

        self.selected_file_number = 0

        self.main_window.show()

    def move_window_backward(self):
        if not self.move_window_offset.toPlainText().isdigit():
            QMessageBox.warning(self, "Error", "Move offset must be an positive integer !")
        elif self.move_window_offset.document().isEmpty() is True:
            QMessageBox.warning(self, "Error", "Select move offset !")
        elif self.moving_window_index - int(self.move_window_offset.toPlainText()) + 1 > 0:
            self.moving_window_index -= int(self.move_window_offset.toPlainText())
            if len(self.moving_window_analysis_result[self.moving_window_index]["SAME_AXES"]) > 0:
                QMessageBox.warning(self, "Warning", "Multiple axes have the same value: \n" +
                                    "".join([str(create_main_axis_string(NoteVectorDirection(
                                        axis.direction % 360)) + "\n")
                                             for axis in self.moving_window_analysis_result[self.moving_window_index]["SAME_AXES"]]))
            if self.moving_window_analysis_result[self.moving_window_index]["MODE_ANGLE_EQUAL_ZERO"]:
                QMessageBox.warning(self, "Warning", "Mode angle equal zero !")
            self.result_information.setText(self.moving_window_analysis_result[self.moving_window_index]["RESULT"])
            self.populate_signature_and_tonal_profiles_results(self.moving_window_analysis_result[self.moving_window_index])
            self.draw_signature_graphics_view(self.signature,
                                              self.ks_results,
                                              self.as_results,
                                              self.t_results)
            self.window_start.setText(str(self.moving_window_analysis_result[self.moving_window_index]["WINDOW_START"]))
            self.window_end.setText(
                str(self.moving_window_analysis_result[self.moving_window_index]["WINDOW_END"]))

    def move_window_forward(self):
        if not self.move_window_offset.toPlainText().isdigit():
            QMessageBox.warning(self, "Error", "Move offset must be an positive integer !")
        elif self.move_window_offset.document().isEmpty() is True:
            QMessageBox.warning(self, "Error", "Select move offset !")
        elif self.moving_window_index + int(self.move_window_offset.toPlainText()) < len(self.moving_window_analysis_result):
            self.moving_window_index += int(self.move_window_offset.toPlainText())
            if len(self.moving_window_analysis_result[self.moving_window_index]["SAME_AXES"]) > 0:
                QMessageBox.warning(self, "Warning", "Multiple axes have the same value: \n" +
                                    "".join([str(create_main_axis_string(NoteVectorDirection(
                                        axis.direction % 360)) + "\n")
                                             for axis in self.moving_window_analysis_result[self.moving_window_index]["SAME_AXES"]]))
            if self.moving_window_analysis_result[self.moving_window_index]["MODE_ANGLE_EQUAL_ZERO"]:
                QMessageBox.warning(self, "Warning", "Mode angle equal zero !")
            self.result_information.setText(self.moving_window_analysis_result[self.moving_window_index]["RESULT"])
            self.populate_signature_and_tonal_profiles_results(self.moving_window_analysis_result[self.moving_window_index])
            self.draw_signature_graphics_view(self.signature,
                                              self.ks_results,
                                              self.as_results,
                                              self.t_results)
            self.window_start.setText(str(self.moving_window_analysis_result[self.moving_window_index]["WINDOW_START"]))
            self.window_end.setText(
                str(self.moving_window_analysis_result[self.moving_window_index]["WINDOW_END"]))


    def expand_window(self):
        if not self.expand_window_offset.toPlainText().isdigit():
            QMessageBox.warning(self, "Error", "Expand offset must be an positive integer !")
        elif self.expand_window_offset.document().isEmpty() is True:
            QMessageBox.warning(self, "Error", "Expand move offset !")
        elif self.expanding_window_index + int(self.expand_window_offset.toPlainText()) < len(self.expanding_window_analysis_result):
            self.expanding_window_index += int(self.expand_window_offset.toPlainText())
            if len(self.expanding_window_analysis_result[self.expanding_window_index]["SAME_AXES"]) > 0:
                QMessageBox.warning(self, "Warning", "Multiple axes have the same value: \n" +
                                    "".join([str(create_main_axis_string(NoteVectorDirection(
                                        axis.direction % 360)) + "\n")
                                             for axis in self.expanding_window_analysis_result[self.expanding_window_index]["SAME_AXES"]]))
            if self.expanding_window_analysis_result[self.expanding_window_index]["MODE_ANGLE_EQUAL_ZERO"]:
                QMessageBox.warning(self, "Warning", "Mode angle equal zero !")
            self.result_information.setText(self.expanding_window_analysis_result[self.expanding_window_index]["RESULT"])
            self.populate_signature_and_tonal_profiles_results(self.expanding_window_analysis_result[self.expanding_window_index])
            self.draw_signature_graphics_view(self.signature,
                                              self.ks_results,
                                              self.as_results,
                                              self.t_results)

            self.window_start.setText(str(self.expanding_window_analysis_result[self.expanding_window_index]["WINDOW_START"]))
            self.window_end.setText(
                str(self.expanding_window_analysis_result[self.expanding_window_index]["WINDOW_END"]))


    def reduce_window(self):
        if not self.expand_window_offset.toPlainText().isdigit():
            QMessageBox.warning(self, "Error", "Reduce offset must be an positive integer !")
        elif self.expand_window_offset.document().isEmpty() is True:
            QMessageBox.warning(self, "Error", "Select reduce offset !")
        elif self.expanding_window_index - int(self.expand_window_offset.toPlainText()) + 1 > 0:
            self.expanding_window_index -= int(self.expand_window_offset.toPlainText())
            if len(self.expanding_window_analysis_result[self.expanding_window_index]["SAME_AXES"]) > 0:
                QMessageBox.warning(self, "Warning", "Multiple axes have the same value: \n" +
                                    "".join([str(create_main_axis_string(NoteVectorDirection(
                                        axis.direction % 360)) + "\n")
                                             for axis in self.expanding_window_analysis_result[self.expanding_window_index]["SAME_AXES"]]))
            if self.expanding_window_analysis_result[self.expanding_window_index]["MODE_ANGLE_EQUAL_ZERO"]:
                QMessageBox.warning(self, "Warning", "Mode angle equal zero !")
            self.result_information.setText(self.expanding_window_analysis_result[self.expanding_window_index]["RESULT"])
            self.populate_signature_and_tonal_profiles_results(self.expanding_window_analysis_result[self.expanding_window_index])
            self.draw_signature_graphics_view(self.signature,
                                              self.ks_results,
                                              self.as_results,
                                              self.t_results)

            self.window_start.setText(str(self.expanding_window_analysis_result[self.expanding_window_index]["WINDOW_START"]))
            self.window_end.setText(
                str(self.expanding_window_analysis_result[self.expanding_window_index]["WINDOW_END"]))


    def populate_signature_and_tonal_profiles_results(self, results):
            self.signature = results["SIGNATURE"]
            self.ks_results = results["KS_RESULTS"]
            self.as_results = results["AS_RESULTS"]
            self.t_results = results["T_RESULTS"]

    def load_file_button_clicker(self):
        self.expanding_window_analysis_result.clear()
        self.moving_window_analysis_result.clear()
        self.filenames, _ = QFileDialog.getOpenFileNames(self, "Open MIDI file", MIDI_FILES_PATH, "MIDI files (*.mid);;")
        file_number = 0
        if len(self.filenames) > 0:
            self.track_list.clear()
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
            .track_manager.calculate_base_rhythmic_value_multiplicity(RHYTHMIC_VALUES[self.min_rhythmic_value.currentText()])
        self.max_number_of_notes.setText(str(self.max_number_of_notes_to_check))
        self.global_track_length = self.files[self.selected_file_number].track_manager.get_operable_range_of_all_tracks()
        self.setup_track_list()
        self.files[self.selected_file_number].track_manager.activate_all_tracks()
        for i in range(self.track_list.count()):
            self.track_list.item(i).setBackground(QColor('green'))
        self.is_track_selected = True



    def track_list_selection_changed(self, item):
        self.selected_track = track_number = int(item.text()[-1:]) - 1
        self.files[self.selected_file_number].track_manager.handle_selection(track_number)
        self.is_track_selected = len(self.files[self.selected_file_number].track_manager.get_selected_tracks_numbers()) > 0
        if (self.files[self.selected_file_number].track_manager.is_track_selected(track_number) is True):
            item.setBackground(QColor('green'))
        else:
            item.setBackground(QColor('white'))

    def set_base_rhythmic_value(self):
        if not self.is_file_selected:
            QMessageBox.warning(self, "Error", "Select file !")
        else:
            self.max_number_of_notes_to_check = self.files[self.selected_file_number].track_manager.calculate_base_rhythmic_value_multiplicity(RHYTHMIC_VALUES[self.min_rhythmic_value.currentText()])
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
            signature_graphic.draw_legend()
            signature_graphic.draw_tonal_profiles_results(ks_results, as_results, t_results)

    def clear_signature_graphics_view(self):
        if self.scene is not None and self.signature_graphic_view is not None:
            self.scene.clear()
            self.signature_graphic_view.viewport().update()

    def save_results_button_clicker(self):
        reader = MidiReader()
        reader.write_results(self, self.moving_window_analysis_result, self.expanding_window_analysis_result)


    def remember_results(self, moving_window_results, expanded_window_results):
        for moving_window_result in moving_window_results:
            self.moving_window_analysis_result.append({"FILENAME":self.files[self.selected_file_number].file.filename,
                                          "SELECTED_TRACKS":self.files[self.selected_file_number].track_manager.get_selected_tracks_numbers(),
                                          "RESULT":moving_window_result})
        for expanded_window_result in expanded_window_results:
            self.expanding_window_analysis_result.append({"FILENAME":self.files[self.selected_file_number].file.filename,
                                          "SELECTED_TRACKS":self.files[self.selected_file_number].track_manager.get_selected_tracks_numbers(),
                                          "RESULT":expanded_window_result})

    def calculate_button_clicker(self):
        if self.number_of_units.document().isEmpty():
            QMessageBox.warning(self, "Error", "Select window !")
            return
        if not self.number_of_units.toPlainText().isdigit():
            QMessageBox.warning(self, "Error", "Window size be an positive integer !")
            return
        number_of_units = int(self.number_of_units.toPlainText())
        if self.is_file_selected == False:
            QMessageBox.warning(self, "Error", "Select file !")
        elif self.is_track_selected == False:
            QMessageBox.warning(self, "Error", "Select track !")
        elif self.max_number_of_notes.document().isEmpty() is True:
            QMessageBox.warning(self, "Error", "Select time window !")
        elif number_of_units < 0 or number_of_units > self.max_number_of_notes_to_check:
            QMessageBox.warning(self, "Error", "Window must match constraints !")
        else:
            self.set_base_rhythmic_value()
            number_of_samples = int(self.max_number_of_notes_to_check / number_of_units)
            remainder_size = self.max_number_of_notes_to_check % number_of_units
            self.moving_window_analysis_result.clear()
            self.expanding_window_analysis_result.clear()
            progress = QProgressDialog("Calculating samples...", "Abort calculation", 0, 100, self)
            progress.resize(800, 400)
            progress.setMinimumDuration(0)
            progress.setModal(True)
            if remainder_size > 0:
                progress_unit = 100/(2 * number_of_samples + 2)
            else:
                progress_unit = 100 / (2 * number_of_samples)
            total_progress = 0
            actual_progress = 0

            actual_window_start = 0
            actual_window_end = 0
            algorithm_info = None
            for actual_position in range(0, number_of_samples):
                actual_window_end += number_of_units
                result_information, algorithm_info, same_axes, mode_angle_equal_zero = self.calculate_results(actual_window_start, actual_window_end)
                self.moving_window_analysis_result.append({"FILENAME":self.files[self.selected_file_number].file.filename,
                                          "SELECTED_TRACKS":self.files[self.selected_file_number].track_manager.get_selected_tracks_numbers(),"RESULT":result_information,
                                                           "ALGORITHM_INFO":algorithm_info, "BASE_RHYTHMIC_VALUE":self.min_rhythmic_value.currentText(),
                                              "SIGNATURE":self.signature, "WINDOW_START":actual_window_start, "WINDOW_END":actual_window_end,
                                              "SAMPLE_CALCULATION_MODE":self.sample_calculation_mode.currentText(), "PROFILE":self.tonal_profiles_type.currentText(),
                                              "KS_RESULTS":self.ks_results, "AS_RESULTS":self.as_results, "T_RESULTS":self.t_results,
                                                           "SAME_AXES":same_axes, "MODE_ANGLE_EQUAL_ZERO":mode_angle_equal_zero})
                actual_window_start = actual_window_end
                actual_progress += progress_unit
                if progress.wasCanceled():
                    self.clear_results()
                    return
                if int(actual_progress) == 1:
                    total_progress += int(actual_progress)
                    actual_progress = 0
                    progress.setValue(total_progress)

            if remainder_size > 0:
                result_information, algorithm_info, same_axes, mode_angle_equal_zero = self.calculate_results(actual_window_start, actual_window_end + remainder_size)
                self.moving_window_analysis_result.append(
                    {"FILENAME":self.files[self.selected_file_number].file.filename,
                                          "SELECTED_TRACKS":self.files[self.selected_file_number].track_manager.get_selected_tracks_numbers(),"RESULT": result_information, "ALGORITHM_INFO": algorithm_info,
                     "BASE_RHYTHMIC_VALUE": self.min_rhythmic_value.currentText(),
                     "SIGNATURE": self.signature, "WINDOW_START": actual_window_start, "WINDOW_END": actual_window_end,
                     "SAMPLE_CALCULATION_MODE": self.sample_calculation_mode.currentText(),
                     "PROFILE": self.tonal_profiles_type.currentText(),
                     "KS_RESULTS": self.ks_results, "AS_RESULTS": self.as_results, "T_RESULTS": self.t_results,
                     "SAME_AXES":same_axes, "MODE_ANGLE_EQUAL_ZERO":mode_angle_equal_zero})
                actual_progress += progress_unit
                if progress.wasCanceled():
                    self.clear_results()
                    return
                if int(actual_progress) == 1:
                    total_progress += int(actual_progress)
                    actual_progress = 0
                    progress.setValue(total_progress)

            actual_window_start = 0
            actual_window_end = 0
            for actual_position in range(0, number_of_samples):
                actual_window_end += number_of_units
                result_information, algorithm_info, same_axes, mode_angle_equal_zero = self.calculate_results(actual_window_start, actual_window_end)
                self.expanding_window_analysis_result.append(
                    {"FILENAME":self.files[self.selected_file_number].file.filename,
                                          "SELECTED_TRACKS":self.files[self.selected_file_number].track_manager.get_selected_tracks_numbers(),"RESULT": result_information, "ALGORITHM_INFO": algorithm_info,
                     "BASE_RHYTHMIC_VALUE": self.min_rhythmic_value.currentText(),
                     "SIGNATURE": self.signature, "WINDOW_START": actual_window_start, "WINDOW_END": actual_window_end,
                     "SAMPLE_CALCULATION_MODE": self.sample_calculation_mode.currentText(),
                     "PROFILE": self.tonal_profiles_type.currentText(),
                     "KS_RESULTS": self.ks_results, "AS_RESULTS": self.as_results, "T_RESULTS": self.t_results,
                     "SAME_AXES":same_axes, "MODE_ANGLE_EQUAL_ZERO":mode_angle_equal_zero})
                actual_progress += progress_unit
                if progress.wasCanceled():
                    self.clear_results()
                    return
                if int(actual_progress) == 1:
                    total_progress += int(actual_progress)
                    actual_progress = 0
                    progress.setValue(total_progress)

            if remainder_size > 0:
                result_information, algorithm_info, same_axes, mode_angle_equal_zero = self.calculate_results(actual_window_end, actual_window_end + remainder_size)
                self.expanding_window_analysis_result.append(
                    {"FILENAME":self.files[self.selected_file_number].file.filename,
                                          "SELECTED_TRACKS":self.files[self.selected_file_number].track_manager.get_selected_tracks_numbers(),"RESULT": result_information, "ALGORITHM_INFO": algorithm_info,
                     "BASE_RHYTHMIC_VALUE": self.min_rhythmic_value.currentText(),
                     "SIGNATURE": self.signature, "WINDOW_START": actual_window_start, "WINDOW_END": actual_window_end,
                     "SAMPLE_CALCULATION_MODE": self.sample_calculation_mode.currentText(),
                     "PROFILE": self.tonal_profiles_type.currentText(),
                     "KS_RESULTS": self.ks_results, "AS_RESULTS": self.as_results, "T_RESULTS": self.t_results,
                     "SAME_AXES":same_axes, "MODE_ANGLE_EQUAL_ZERO":mode_angle_equal_zero})
            progress.setValue(100)

            if len(self.expanding_window_analysis_result[self.expanding_window_index]["SAME_AXES"]) > 0:
                QMessageBox.warning(self, "Warning", "Multiple axes have the same value: \n" +
                                    "".join([str(create_main_axis_string(NoteVectorDirection(
                                        axis.direction % 360)) + "\n")
                                             for axis in self.expanding_window_analysis_result[0][
                                                 "SAME_AXES"]]))
            self.result_information.setText(self.expanding_window_analysis_result[0]["RESULT"])
            self.populate_signature_and_tonal_profiles_results(self.moving_window_analysis_result[self.moving_window_index])
            self.draw_signature_graphics_view(self.signature,
                                              self.ks_results,
                                              self.as_results,
                                              self.t_results)
            self.window_start.setText(str(self.expanding_window_analysis_result[0]["WINDOW_START"]))
            self.window_end.setText(
                str(self.expanding_window_analysis_result[0]["WINDOW_END"]))


    def clear_results(self):
        self.moving_window_analysis_result.clear()
        self.expanding_window_analysis_result.clear()
        self.moving_window_index = 0
        self.expanding_window_index = 0
        self.window_start.setText("")
        self.window_end.setText("")
        self.clear_signature_graphics_view()
        self.result_information.setText("unknown")

    def calculate_results(self, actual_window_start, actual_window_end):
        algorithm_info = AlgorithmInfo(
            algorithm_type=ALGORITHM_NAMES[self.algorithm_type_dropdown.currentText()],
            sample_calculation_mode=SAMPLE_CALCULATION_MODES[self.sample_calculation_mode.currentText()],
            profile=TONAL_PROFILE_NAMES[self.tonal_profiles_type.currentText()])
        result_information, self.signature, same_axes, mode_angle_equal_zero = self.algorithm_manager.execute_algorithm(algorithm_info,
                                                                                      self.files[
                                                                                          self.selected_file_number].track_manager.calculate_sample_vector(
                                                                                          actual_window_start,
                                                                                          actual_window_end,
                                                                                          SAMPLE_CALCULATION_MODES[
                                                                                              self.sample_calculation_mode.currentText()],
                                                                                          self.min_rhythmic_value.currentText()))

        self.ks_results, _, _, _ = self.algorithm_manager.execute_algorithm(AlgorithmInfo(
            algorithm_type=Algorithm.CLASSIC_TONAL_PROFILES,
            sample_calculation_mode=SAMPLE_CALCULATION_MODES[self.sample_calculation_mode.currentText()],
            profile=Profile.KS),
            self.files[self.selected_file_number].track_manager.calculate_sample_vector(
                actual_window_start, actual_window_end,
                SAMPLE_CALCULATION_MODES[
                    self.sample_calculation_mode.currentText()],
                self.min_rhythmic_value.currentText()))

        self.as_results, _, _, _ = self.algorithm_manager.execute_algorithm(AlgorithmInfo(
            algorithm_type=Algorithm.CLASSIC_TONAL_PROFILES,
            sample_calculation_mode=SAMPLE_CALCULATION_MODES[self.sample_calculation_mode.currentText()],
            profile=Profile.AS),
            self.files[self.selected_file_number].track_manager.calculate_sample_vector(
                actual_window_start, actual_window_end,
                SAMPLE_CALCULATION_MODES[
                    self.sample_calculation_mode.currentText()],
                self.min_rhythmic_value.currentText()))

        self.t_results, _, _, _ = self.algorithm_manager.execute_algorithm(AlgorithmInfo(
            algorithm_type=Algorithm.CLASSIC_TONAL_PROFILES,
            sample_calculation_mode=SAMPLE_CALCULATION_MODES[self.sample_calculation_mode.currentText()],
            profile=Profile.T),
            self.files[self.selected_file_number].track_manager.calculate_sample_vector(
                actual_window_start, actual_window_end,
                SAMPLE_CALCULATION_MODES[
                    self.sample_calculation_mode.currentText()],
                self.min_rhythmic_value.currentText()))

        return result_information, algorithm_info, same_axes, mode_angle_equal_zero

'''
Bug z nie wyświetlaniem tonacji dla wartości przy końcu zakresu, przy zakresie określonym przez wyświetlaną wartość
jest powodowany złym obliczeniem zakresu - pod koniec już nie ma nut.
Występuje dla niewielkich wartości rytmicznych - poniżej ósemki.
'''
