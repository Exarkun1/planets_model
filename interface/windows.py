from PyQt6 import QtCore, QtWidgets

import interface.widgets as widgets

class UiMainWindow:
    """
    Класс, добавляющий в окно визуальные элементы.
    """
    def setupUi(self):
        """
        Метод инициализации визуальных элементов.
        """
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

        self.table = widgets.Table(cols=7)
        self.table.add_texts(["X", "Y", "Z", "Vx", "Vy", "Vz", "M"])
        self.add_row_button = QtWidgets.QPushButton("ADD ROW")
        self.delete_row_button = QtWidgets.QPushButton("DELETE ROW")

        self.method_list = QtWidgets.QComboBox()
        self.method_list.addItems(["Euler", "Euler Kramer", "Biman", "Vernele"])

        self.time_edit_line = QtWidgets.QLineEdit()
        self.ht_edit_line = QtWidgets.QLineEdit()
        self.sidebar_box.add_widget(
            widgets.Form(widgets=[
                widgets.HBox(widgets=[self.add_row_button, self.delete_row_button]),
                self.table,
                self.method_list,
                widgets.HBox(widgets=[
                    widgets.VBox(widgets=[QtWidgets.QLabel("Time, sec"), self.time_edit_line]),
                    widgets.VBox(widgets=[QtWidgets.QLabel("Ht, sec"), self.ht_edit_line])
                ])
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

class TimerMainWindow:
    """
    Класс, добавляющий в окно таймер.
    """
    def setupTimer(self, 
                   interval : int = 100):
        """
        Метод инициализации таймера.

        Args:
            interval: промежуток времени между срабатываниями таймера.
        """
        self.frame_timer = QtCore.QTimer()
        self.frame_timer.setInterval(interval)