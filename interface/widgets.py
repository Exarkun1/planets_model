from PyQt6 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class Graphic3D(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection="3d")
        super(Graphic3D, self).__init__(figure=fig)

class Rect(QtWidgets.QWidget):
    def __init__(self, width=None, height=None):
        super(Rect, self).__init__()
        if isinstance(width, int):
            self.setMaximumWidth(width)
        if isinstance(height, int):
            self.setMaximumHeight(height)

class AddableWidget:
    def add_widget(self, widget : QtWidgets.QWidget):
        self.lay.addWidget(widget)

    def add_widgets(self, widgets : list[QtWidgets.QWidget]):
        if widgets == None:
            return
        for widget in widgets:
            self.add_widget(widget)

class HBox(Rect, AddableWidget):
    def __init__(self, width=None, height=None, widgets:list[QtWidgets.QWidget]=None):
        super(__class__, self).__init__(width, height)
        self.lay = QtWidgets.QHBoxLayout(self)
        self.add_widgets(widgets)

class VBox(Rect, AddableWidget):
    def __init__(self, width=None, height=None, widgets:list[QtWidgets.QWidget]=None):
        super(__class__, self).__init__(width, height)
        self.lay = QtWidgets.QVBoxLayout(self)
        self.add_widgets(widgets)

class Form(Rect, AddableWidget):
    def __init__(self, width=None, height=None, widgets:list[QtWidgets.QWidget]=None):
        super(__class__, self).__init__(width, height)
        self.lay = QtWidgets.QFormLayout(self)
        self.add_widgets(widgets)

class TextLine(QtWidgets.QLineEdit):
    def __init__(self):
        super(__class__, self).__init__()
        self.setEnabled(True)
        self.setText("")
        self.setReadOnly(True)