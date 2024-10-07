from PyQt6 import QtCore, QtWidgets
from interface.windows import UiMainWindow, TimerMainWindow
from application.actions import update_window, reset_timer

class MainWindow(QtWidgets.QMainWindow, UiMainWindow, TimerMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        self.setupUi()
        self.setupTimer(100)

        self.frame_timer.timeout.connect(update_window(self))
        self.play_button.clicked.connect(lambda: self.frame_timer.start())
        self.pause_button.clicked.connect(lambda: self.frame_timer.stop())
        self.reset_button.clicked.connect(reset_timer(self))