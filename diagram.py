import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(BASE_DIR, "libs")
sys.path.insert(0, LIBS_DIR)
from pyqtgraph import PlotWidget
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QMenu


class Diagram(PlotWidget):
    def __init__(self, background = "default", *args, **kargs):
            pwArgList = ['title', 'labels', 'name', 'left', 'right', 'top', 'bottom', 'background']
            pwArgs = {}
            dataArgs = {}
            for k in kargs:
                if k in pwArgList:
                    pwArgs[k] = kargs[k]
                else:
                    dataArgs[k] = kargs[k]
            windowTitle = pwArgs.pop("title", "PlotWidget")
            super().__init__(**pwArgs)
            self.setWindowTitle(windowTitle)
            self.setBackground(background)
            self.showGrid(x = True, y = True)
            self.setMenuEnabled(False)
    
    def draw(self, *args, **kwargs):
        self.plot(*args, symbol='o', **kwargs)

    def setList(self, x, y):
        self.clear()
        self.draw(x, y)