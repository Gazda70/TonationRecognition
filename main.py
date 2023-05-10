import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, uic
from view.basic_ui import UI_MainPage

def main():
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    main_ui_page = UI_MainPage()
    widget.addWidget(main_ui_page)
    w = 1800
    h = 900
    widget.resize(w, h)
#    widget.show()
    app.exec_()

if ( __name__ == '__main__' ):
    main()