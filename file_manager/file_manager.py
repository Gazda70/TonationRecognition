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


def read_config_file(config_file_name):
    config_file = open(config_file_name)
    config = []
    for line in config_file:
        new_file_config = line.split(':')
        config.append({"FILENAME":new_file_config[0], "TONATION":new_file_config[1], "BASE_RHYTMIC_VALUE":new_file_config[2].strip()})
    return config


self.all_files_results.append({"FILENAME": file.file.filename, "NOTES_TO_DETERMINE": sample_size_to_find_tonation,
                               "DECISION_CHANGES": decision_changes_counter,
                               "KS_NOTES_TO_DETERMINE": sample_size_to_find_tonation_profile_KS,
                               "KS_DECISION_CHANGES": decision_change_counter_profile_KS,
                               "AS_NOTES_TO_DETERMINE": sample_size_to_find_tonation_profile_AS,
                               "AS_DECISION_CHANGES": decision_change_counter_profile_AS,
                               "T_NOTES_TO_DETERMINE": sample_size_to_find_tonation_profile_T,
                               "T_DECISION_CHANGES": decision_change_counter_profile_T, })

def write_multifile_results(results):
    # filename = QFileDialog.getSaveFileName(ui_object, 'Save File',
    #                                        'E:\\PracaMagisterska\\midi\\Pliki MIDI\\Bach\\WTC_I\\experiments_results\\sof_profile_quantity',
    #                                        ".xlsx(*.xlsx)")
    # Workbook() takes one, non-optional, argument
    # which is the filename that we want to create.
    # if filename[0] == "":
    #     return
    workbook = xlsxwriter.Workbook('results.xlsx')

    # The workbook object is then used to add new
    # worksheet via the add_worksheet() method.
    worksheet = workbook.add_worksheet()
    row_counter = 1
    worksheet.write('A' + str(row_counter), "Number")
    worksheet.write('B' + str(row_counter), "Filename")
    worksheet.write('C' + str(row_counter), "Main algorithm notes to determine tonation")
    worksheet.write('D' + str(row_counter), "Main algorithm number of decision changes")
    worksheet.write('E' + str(row_counter), "KS notes to determine tonation")
    worksheet.write('F' + str(row_counter), "KS number of decision changes")
    worksheet.write('G' + str(row_counter), "AS notes to determine tonation")
    worksheet.write('H' + str(row_counter), "AS number of decision changes")
    worksheet.write('I' + str(row_counter), "T notes to determine tonation")
    worksheet.write('J' + str(row_counter), "T number of decision changes")
    row_counter += 1
    for result in results:
        worksheet.write('A' + str(row_counter), str(row_counter))
        worksheet.write('B' + str(row_counter), result["FILENAME"])
        worksheet.write('C' + str(row_counter), result["NOTES_TO_DETERMINE"])
        worksheet.write('D' + str(row_counter), result["DECISION_CHANGES"])
        worksheet.write('E' + str(row_counter), result["KS_NOTES_TO_DETERMINE"])
        worksheet.write('F' + str(row_counter), result["KS_DECISION_CHANGES"])
        worksheet.write('G' + str(row_counter), result["AS_NOTES_TO_DETERMINE"])
        worksheet.write('H' + str(row_counter), result["AS_DECISION_CHANGES"])
        worksheet.write('I' + str(row_counter), result["T_NOTES_TO_DETERMINE"])
        worksheet.write('J' + str(row_counter), result["T_DECISION_CHANGES"])
        row_counter += 1
    workbook.close()


class MidiReader:

    def read_file(self, midi_path):
        new_file = MidiFile(midi_path, clip=True)
        track_manager = TrackManager()
        track_manager.process_file(new_file)

        return new_file, track_manager

    def write_results(self, ui_object, moving_window_results, expanding_window_results):
        filename = QFileDialog.getSaveFileName(ui_object, 'Save File', 'E:\\PracaMagisterska\\midi\\Pliki MIDI\\Bach\\WTC_I\\experiments_results\\sof_profile_quantity', ".xlsx(*.xlsx)")
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
        previous_tonation = None
        previous_tonation_profile_KS = None
        previous_tonation_profile_AS = None
        previous_tonation_profile_T = None
        decision_change_index = 1
        decision_change_index_profile_KS = 1
        decision_change_index_profile_AS = 1
        decision_change_index_profile_T = 1
        decision_change_counter = 0
        decision_change_counter_profile_KS = 0
        decision_change_counter_profile_AS = 0
        decision_change_counter_profile_T = 0
        worksheet.write('I' + str(multiple_axes_cases_number), "MAIN ALGORITHM DECISION CHANGES")
        decision_change_index += 1
        worksheet.write('K' + str(decision_change_index_profile_KS), "KS PROFILE DECISION CHANGES")
        decision_change_index_profile_KS += 1
        worksheet.write('M' + str(decision_change_index_profile_AS), "AS PROFILE DECISION CHANGES")
        decision_change_index_profile_AS += 1
        worksheet.write('O' + str(decision_change_index_profile_T), "T PROFILE DECISION CHANGES")
        decision_change_index_profile_T += 1
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
                decision_change_counter += 1
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

            if previous_tonation_profile_KS is not None and previous_tonation_profile_KS != result["KS_RESULTS"]:
                decision_change_counter_profile_KS += 1
                worksheet.write('K' + str(decision_change_index_profile_KS), "DECISION CHANGE")
                worksheet.write('L' + str(decision_change_index_profile_KS), str(previous_tonation_profile_KS) + "->" + result["KS_RESULTS"])
                decision_change_index_profile_KS += 1
                worksheet.write('K' + str(decision_change_index_profile_KS), "WINDOW_START")
                worksheet.write('L' + str(decision_change_index_profile_KS), result["WINDOW_START"])
                decision_change_index_profile_KS += 1
                worksheet.write('K' + str(decision_change_index_profile_KS), "WINDOW_END")
                worksheet.write('L' + str(decision_change_index_profile_KS), result["WINDOW_END"])
                decision_change_index_profile_KS += 4
            previous_tonation_profile_KS = result["KS_RESULTS"]

            worksheet.write('A' + str(analysis_result_number), "AS_RESULTS")
            worksheet.write('B' + str(analysis_result_number), result["AS_RESULTS"])
            analysis_result_number += 1

            if previous_tonation_profile_AS is not None and previous_tonation_profile_AS != result["AS_RESULTS"]:
                decision_change_counter_profile_AS += 1
                worksheet.write('M' + str(decision_change_index_profile_AS), "DECISION CHANGE")
                worksheet.write('N' + str(decision_change_index_profile_AS), str(previous_tonation_profile_AS) + "->" + result["AS_RESULTS"])
                decision_change_index_profile_AS += 1
                worksheet.write('M' + str(decision_change_index_profile_AS), "WINDOW_START")
                worksheet.write('N' + str(decision_change_index_profile_AS), result["WINDOW_START"])
                decision_change_index_profile_AS += 1
                worksheet.write('M' + str(decision_change_index_profile_AS), "WINDOW_END")
                worksheet.write('N' + str(decision_change_index_profile_AS), result["WINDOW_END"])
                decision_change_index_profile_AS += 4
            previous_tonation_profile_AS = result["AS_RESULTS"]

            worksheet.write('A' + str(analysis_result_number), "T_RESULTS")
            worksheet.write('B' + str(analysis_result_number), result["T_RESULTS"])

            if previous_tonation_profile_T is not None and previous_tonation_profile_T != result["T_RESULTS"]:
                decision_change_counter_profile_T += 1
                worksheet.write('O' + str(decision_change_index_profile_T), "DECISION CHANGE")
                worksheet.write('P' + str(decision_change_index_profile_T), str(previous_tonation_profile_T) + "->" + result["T_RESULTS"])
                decision_change_index_profile_T += 1
                worksheet.write('O' + str(decision_change_index_profile_T), "WINDOW_START")
                worksheet.write('P' + str(decision_change_index_profile_T), result["WINDOW_START"])
                decision_change_index_profile_T += 1
                worksheet.write('O' + str(decision_change_index_profile_T), "WINDOW_END")
                worksheet.write('P' + str(decision_change_index_profile_T), result["WINDOW_END"])
                decision_change_index_profile_T += 4
            previous_tonation_profile_T = result["T_RESULTS"]

            analysis_result_number += 2

        worksheet.write('I' + str(decision_change_index), "MAIN ALGORITHM DECISION CHANGE COUNT")
        worksheet.write('J' + str(decision_change_index), decision_change_counter)
        worksheet.write('K' + str(decision_change_index_profile_KS), "KS DECISION CHANGE COUNT")
        worksheet.write('L' + str(decision_change_index_profile_KS), decision_change_counter_profile_KS)
        worksheet.write('M' + str(decision_change_index_profile_AS), "AS DECISION CHANGE COUNT")
        worksheet.write('N' + str(decision_change_index_profile_AS), decision_change_counter_profile_AS)
        worksheet.write('O' + str(decision_change_index_profile_T), "T DECISION CHANGE COUNT")
        worksheet.write('P' + str(decision_change_index_profile_T), decision_change_counter_profile_T)


        # Finally, close the Excel file
        # via the close() method.
        workbook.close()