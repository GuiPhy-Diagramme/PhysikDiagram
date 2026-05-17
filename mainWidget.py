import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(BASE_DIR, "libs")
sys.path.insert(0, LIBS_DIR)
from PySide6.QtWidgets import QWidget, QGridLayout
from diagram import Diagram
from pointList import PointList


class MainWidget(QWidget):
    def __init__(self, comFunc):
        super().__init__()
        self.__listWidget = PointList(comFunc)
        background = self.palette().color(self.backgroundRole())
        self.__plot = Diagram(background)
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.__listWidget, 0, 0)
        layout.addWidget(self.__plot, 0, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)

    def updateList(self, x, y):
        self.__plot.setList(x, y)
        self.__listWidget.setList(x, y)
    
    def get_plot(self):
        return self.__plot