from dataclasses import dataclass
from PyQt5.QtWidgets import QFileDialog
from mido import MidiFile

from file_manager.track_manager import TrackManager
import xlsxwriter

from model.definitions import NoteVectorDirection
from utils.mappings import create_main_axis_string


@dataclass
class FileInfo:
    file:MidiFile
    track_manager:TrackManager
    is_selected:bool
    file_number:int
class MidiReader:

    def read_file(self, midi_path):
        new_file = MidiFile(midi_path, clip=True)
        track_manager = TrackManager()
        track_manager.process_file(new_file)

        return new_file, track_manager


    def write_results(self, ui_object, moving_window_results, expanding_window_results):
        filename = QFileDialog.getSaveFileName(ui_object, 'Save File', '', ".xlsx(*.xlsx)")
        # Workbook() takes one, non-optional, argument
        # which is the filename that we want to create.
        if filename[0] == "":
            return
        workbook = xlsxwriter.Workbook(filename[0])

        # The workbook object is then used to add new
        # worksheet via the add_worksheet() method.
        worksheet = workbook.add_worksheet()
        analysis_result_number = 1
        multiple_axes_cases_number = 1
        previous_tonation = None
        worksheet.write('E' + str(multiple_axes_cases_number), "MOVING_WINDOW_RESULTS")
        multiple_axes_cases_number += 1
        for result in moving_window_results:
            # Use the worksheet object to write
            # data via the write() method.
            if len(result["SAME_AXES"]) > 0:
                worksheet.write('E' + str(multiple_axes_cases_number), "SAME_AXES")
                worksheet.write('F' + str(multiple_axes_cases_number), "".join([str(create_main_axis_string(NoteVectorDirection(
                                        axis.direction % 360)) + "\n")
                                             for axis in result["SAME_AXES"]]))
                multiple_axes_cases_number += 1
                worksheet.write('E' + str(multiple_axes_cases_number), "WINDOW_START")
                worksheet.write('F' + str(multiple_axes_cases_number), result["WINDOW_START"])
                multiple_axes_cases_number += 1

                worksheet.write('E' + str(multiple_axes_cases_number), "WINDOW_END")
                worksheet.write('F' + str(multiple_axes_cases_number), result["WINDOW_END"])
                multiple_axes_cases_number += 4
            worksheet.write('A' + str(analysis_result_number), "FILENAME")
            worksheet.write('B' + str(analysis_result_number), result["FILENAME"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "SELECTED_TRACKS")
            worksheet.write('B' + str(analysis_result_number), ''.join(str(result["SELECTED_TRACKS"])))
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "WINDOW_START")
            worksheet.write('B' + str(analysis_result_number), result["WINDOW_START"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "WINDOW_END")
            worksheet.write('B' + str(analysis_result_number), result["WINDOW_END"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "BASE_RHYTHMIC_VALUE")
            worksheet.write('B' + str(analysis_result_number), result["BASE_RHYTHMIC_VALUE"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "ALGORITHM_NAME")
            worksheet.write('B' + str(analysis_result_number), result["ALGORITHM_INFO"].algorithm_type.name)
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "SAMPLE_CALCULATION_MODE")
            worksheet.write('B' + str(analysis_result_number), result["SAMPLE_CALCULATION_MODE"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "PROFILE")
            worksheet.write('B' + str(analysis_result_number), result["PROFILE"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "RESULT")
            worksheet.write('B' + str(analysis_result_number), result["RESULT"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "KS_RESULTS")
            worksheet.write('B' + str(analysis_result_number), result["KS_RESULTS"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "AS_RESULTS")
            worksheet.write('B' + str(analysis_result_number), result["AS_RESULTS"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "T_RESULTS")
            worksheet.write('B' + str(analysis_result_number), result["T_RESULTS"])

            analysis_result_number += 2

        multiple_axes_cases_number = 0
        worksheet.write('E' + str(multiple_axes_cases_number), "EXPANDING_WINDOW_RESULTS")
        multiple_axes_cases_number += 1
        decision_change_index = 1
        for result in expanding_window_results:
            # Use the worksheet object to write
            # data via the write() method.
            if len(result["SAME_AXES"]) > 0:
                worksheet.write('G' + str(multiple_axes_cases_number), "SAME_AXES")
                worksheet.write('H' + str(multiple_axes_cases_number), "".join([str(create_main_axis_string(NoteVectorDirection(
                                        axis.direction % 360)) + "\n")
                                             for axis in result["SAME_AXES"]]))
                multiple_axes_cases_number += 1
                worksheet.write('G' + str(multiple_axes_cases_number), "WINDOW_START")
                worksheet.write('H' + str(multiple_axes_cases_number), result["WINDOW_START"])
                multiple_axes_cases_number += 1

                worksheet.write('G' + str(multiple_axes_cases_number), "WINDOW_END")
                worksheet.write('H' + str(multiple_axes_cases_number), result["WINDOW_END"])
                multiple_axes_cases_number += 4
            if previous_tonation is not None and previous_tonation != result["RESULT"]:
                worksheet.write('I' + str(decision_change_index), "DECISION CHANGE")
                worksheet.write('J' + str(decision_change_index), str(previous_tonation) + "->" + result["RESULT"])
                decision_change_index += 1
                worksheet.write('I' + str(decision_change_index), "WINDOW_START")
                worksheet.write('J' + str(decision_change_index), result["WINDOW_START"])
                decision_change_index += 1
                worksheet.write('I' + str(decision_change_index), "WINDOW_END")
                worksheet.write('J' + str(decision_change_index), result["WINDOW_END"])
                decision_change_index += 4
            previous_tonation = result["RESULT"]
            worksheet.write('A' + str(analysis_result_number), "FILENAME")
            worksheet.write('B' + str(analysis_result_number), result["FILENAME"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "SELECTED_TRACKS")
            worksheet.write('B' + str(analysis_result_number), ''.join(str(result["SELECTED_TRACKS"])))
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "WINDOW_START")
            worksheet.write('B' + str(analysis_result_number), result["WINDOW_START"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "WINDOW_END")
            worksheet.write('B' + str(analysis_result_number), result["WINDOW_END"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "BASE_RHYTHMIC_VALUE")
            worksheet.write('B' + str(analysis_result_number), result["BASE_RHYTHMIC_VALUE"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "ALGORITHM_NAME")
            worksheet.write('B' + str(analysis_result_number), result["ALGORITHM_INFO"].algorithm_type.name)
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "SAMPLE_CALCULATION_MODE")
            worksheet.write('B' + str(analysis_result_number), result["SAMPLE_CALCULATION_MODE"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "RESULT")
            worksheet.write('B' + str(analysis_result_number), result["RESULT"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "PROFILE")
            worksheet.write('B' + str(analysis_result_number), result["PROFILE"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "KS_RESULTS")
            worksheet.write('B' + str(analysis_result_number), result["KS_RESULTS"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "AS_RESULTS")
            worksheet.write('B' + str(analysis_result_number), result["AS_RESULTS"])
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "T_RESULTS")
            worksheet.write('B' + str(analysis_result_number), result["T_RESULTS"])

            analysis_result_number += 2


        # Finally, close the Excel file
        # via the close() method.
        workbook.close()