from PyQt6 import QtCore, QtWidgets

import interface.widgets as widgets
from application.utils import AppPapams
import gravity.difference_schemes as ds

class UiMainWindow:
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1042, 571)
        self.central_box = widgets.HBox()
        self.graphic_box = widgets.Graphic3D(width=5, height=4, dpi=100)
        self.sidebar_box = widgets.Form(width=700)

        self.time_sec_line = widgets.TextLine()
        self.time_max_sec_line = widgets.TextLine()
        self.sidebar_box.add_widget(
            widgets.HBox(widgets=[
                QtWidgets.QLabel("Time, sec"), 
                self.time_sec_line,
                QtWidgets.QLabel("of"), 
                self.time_max_sec_line
            ])
        )
        
        self.time_day_line = widgets.TextLine()
        self.time_max_day_line = widgets.TextLine()
        self.sidebar_box.add_widget(
            widgets.HBox(widgets=[
                QtWidgets.QLabel("Time, day"), 
                self.time_day_line,
                QtWidgets.QLabel("of"), 
                self.time_max_day_line
            ])
        )

        self.energy_line = widgets.TextLine()
        self.sidebar_box.add_widget(
            widgets.VBox(widgets=[
                QtWidgets.QLabel("Total energy, J"),
                self.energy_line
            ])
        )

        self.play_button = QtWidgets.QPushButton("PLAY")
        self.pause_button = QtWidgets.QPushButton("PAUSE")
        self.reset_button = QtWidgets.QPushButton("RESET")
        self.sidebar_box.add_widget(
            widgets.HBox(widgets=[
                self.play_button,
                self.pause_button,
                self.reset_button
            ])
        )

        self.setCentralWidget(self.central_box)
        self.central_box.add_widget(self.sidebar_box)
        self.central_box.add_widget(self.graphic_box)


class MainWindow(QtWidgets.QMainWindow, UiMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        self.setupUi()
        self.app = AppPapams()