from dataclasses import dataclass
from PyQt5.QtWidgets import QFileDialog
from mido import MidiFile

from file_manager.track_manager import TrackManager
import xlsxwriter
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


    def write_results(self, ui_object, analysis_results):
        filename = QFileDialog.getSaveFileName(ui_object, 'Save File', '', ".xlsx(*.xlsx)")
        # Workbook() takes one, non-optional, argument
        # which is the filename that we want to create.
        workbook = xlsxwriter.Workbook(filename[0])

        # The workbook object is then used to add new
        # worksheet via the add_worksheet() method.
        worksheet = workbook.add_worksheet()
        analysis_result_number = 1
        for result in analysis_results:
            # Use the worksheet object to write
            # data via the write() method.
            worksheet.write('A' + str(analysis_result_number), "FILENAME")
            worksheet.write('B' + str(analysis_result_number), filename[0])
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
            worksheet.write('B' + str(analysis_result_number), result["ALGORITHM_INFO"].sample_calculation_mode.name)
            analysis_result_number += 1

            worksheet.write('A' + str(analysis_result_number), "PROFILE")
            worksheet.write('B' + str(analysis_result_number), result["ALGORITHM_INFO"].profile.name)
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