import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(BASE_DIR, "libs")
sys.path.insert(0, LIBS_DIR)
from pyqtgraph import PlotWidget
from pyqtgraph.graphicsItems.ViewBox import ViewBox
from pyqtgraph.graphicsItems.ViewBox.ViewBoxMenu import ViewBoxMenu
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QMenu

class CustomViewBox(ViewBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def export(self, exporter_index):
        exporter_attrs = EXPORTER_LIST[exporter_index]
        filename, _ = QFileDialog.getSaveFileName(
            None,
            "Als " + exporter_attrs[1] + " exportieren",
            "",
            exporter_attrs[1] + " Dateien " + exporter_attrs[2]
        )
        if not filename:
            return
        exporter = exporter_attrs[0](self)
        exporter.export(filename)

    def raiseContextMenu(self, ev):
        menu = self.getMenu(ev)
        if menu is not None:
            menu.clear()
            export_menu = QMenu("Exportieren", menu)
            export_menu.addActions([
                QAction(f"Als {exporter_attrs[1]} exportieren", menu) for exporter_attrs in EXPORTER_LIST
            ])
            for i, action in enumerate(export_menu.actions()):
                action.triggered.connect(lambda checked=False, i=i: self.export(i))
            menu.addMenu(export_menu)
            menu.popup(ev.screenPos().toPoint())


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
            super().__init__(viewBox=CustomViewBox(), **pwArgs)
            self.setWindowTitle(windowTitle)
            self.setBackground(background)
            self.showGrid(x = True, y = True)
    
    def draw(self, *args, **kwargs):
        self.plot(*args, symbol='o', **kwargs)

    def setList(self, x, y):
        self.clear()
        self.draw(x, y)