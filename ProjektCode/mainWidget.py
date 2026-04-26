from PySide6.QtWidgets import QWidget, QGridLayout
from diagram import Diagram
from pointList import PointList


class MainWidget(QWidget):
    def __init__(self, comFunc):
        super().__init__()
        self._listWidget = PointList(comFunc)
        background = self.palette().color(self.backgroundRole())
        self._plot = Diagram(background)
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self._listWidget, 0, 0)  # list widget goes in bottom-left
        layout.addWidget(self._plot, 0, 1)  # plot goes on right side, spanning
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)

    def updateList(self, x, y):
        self._plot.setList(x, y)
        self._listWidget.setList(x, y)