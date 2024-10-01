import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem
from PyQt6 import QtGui
from mainWindow import Ui_MainWindow
import pyqtgraph as pg
import sys

bodies = []
bodies_count = 1

class MainWindow_(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.Button_AddBody.clicked.connect(self.AddBody)
        self.Button_DelBody.clicked.connect(self.DelBody)


        self.show()

    def AddBody(self):
        global bodies_count
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        bodies_count = bodies_count + 1
        return
    def DelBody(self):
        if len(self.tableWidget.selectedIndexes()) != 1:
            index = self.tableWidget.rowCount() - 1
        else:
            index = self.tableWidget.selectedIndexes()[0].row()
        self.tableWidget.removeRow(index)
        return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow_()
    sys.exit(app.exec())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
