import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Drawing Tutorial"
        self.top= 150
        self.left= 150
        self.width = 500
        self.height = 500
        self.InitWindow()
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 8, Qt.SolidLine))
        painter.drawEllipse(40, 40, 400, 400)
        painter.drawLine(40, 220, 220, 220)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())