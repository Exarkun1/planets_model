from PyQt6 import QtWidgets
from interface.windows import UiMainWindow, TimerMainWindow
import application.actions as act

class MainWindow(QtWidgets.QMainWindow, UiMainWindow, TimerMainWindow):
    """
    Класс основного окна.
    """
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        self.setupUi()
        self.setupTimer(100)

        self.frame_timer.timeout.connect(act.update_window(self))
        self.play_button.clicked.connect(lambda: self.frame_timer.start())
        self.pause_button.clicked.connect(lambda: self.frame_timer.stop())
        self.reset_button.clicked.connect(act.reset_timer(self))
        self.add_row_button.clicked.connect(act.add_row(self))
        self.delete_row_button.clicked.connect(act.delete_row(self))