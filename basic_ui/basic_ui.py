import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog
from PyQt5 import uic


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi("file_load.ui", self)

        self.button = self.findChild(QPushButton, "pushButton")
        self.button.clicked.connect(self.clicker)

        self.show()


    def clicker(self):
        fname = QFileDialog.getOpenFileName()
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()