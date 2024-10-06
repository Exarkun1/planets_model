import sys
from PyQt6 import QtWidgets

from interface.windows import MainWindow
from application.utils import AppPapams

if __name__ == "__main__":
    AppPapams()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())