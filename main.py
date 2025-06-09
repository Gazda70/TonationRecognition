import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from view.application_mode_selection_window import Ui_ApplicationModeSelectionWindow

def main():
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    main_ui_page = Ui_ApplicationModeSelectionWindow()
    widget.addWidget(main_ui_page)
    w = 1800
    h = 900
    widget.resize(w, h)
    app.exec_()

if ( __name__ == '__main__' ):
    main()