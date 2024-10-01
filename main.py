import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtGui
from mainWindow import Ui_MainWindow
import pyqtgraph as pg
import sys

class MainWindow_(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.ButtonAccept.clicked.connect(self.AcceptBodies)

        self.show()

    def AcceptBodies(self):
        return



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow_()
    sys.exit(app.exec())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
