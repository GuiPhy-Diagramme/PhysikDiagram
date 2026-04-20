import sys
import argparse
#import pandas as pd
import pyqtgraph as pg
import time
from dateutil import parser
from PySide6.QtGui import QCursor, QFont, QIcon, QKeySequence, QPalette, QRegion
from PySide6 import QtWidgets
from PySide6.QtCore import Qt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, widget = None):
        super().__init__()
        self.setWindowTitle("Eartquakes information")
        if widget:
            self.setCentralWidget(widget)
        # Menu
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("File")

        # Exit QAction
        file_menu.addAction(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit),
                            "Exit", QKeySequence.StandardKey.Quit, self.close)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)


class Diagramm(pg.PlotWidget):
    def __init__(self, *args, **kargs):
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
            if len(args) > 0 or len(dataArgs) > 0:
                self.plot(*args, **dataArgs)
    
    def setList(self, x, y):
        self.clear()
        self.plot(x, y)


class GraphItemList(QtWidgets.QWidget):
    def __init__(self, *args, **kargs):
        super().__init__(*args, *kargs)
        self.x_list = QtWidgets.QListWidget()
        self.y_list = QtWidgets.QListWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.x_list)
        layout.addWidget(self.y_list)
        self.setLayout(layout)
    
    def setList(self, x, y):
        for list_widget, elements in ((self.x_list, x), (self.y_list, y)):
            list_widget.clear()
            for item in elements:
                list_widget.addItem(str(item))


def read_data(fname):
    # Read the CSV content
    df = pd.read_csv(fname)

    # Remove wrong magnitudes
    df = df.drop(df[df.mag < 0].index)
    magnitudes = df["mag"]

    # Get timestamp transformed to our timezone
    times = df["time"]
    epochs = []
    for strtime in times:
        epochs.append(parser.parse(strtime).timestamp())

    return epochs, list(magnitudes)


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        btn = QtWidgets.QPushButton('Werte hinzufügen')
        text_x = QtWidgets.QLineEdit(placeholderText='X Wert')
        text_y = QtWidgets.QLineEdit(placeholderText="Y Wert")
        self.listWidget = GraphItemList()
        self.plot = Diagramm()
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        layout.addWidget(text_x, 0, 0)
        layout.addWidget(text_y, 0, 1)
        layout.addWidget(btn, 1, 0, 1, 2)
        layout.addWidget(self.listWidget, 2, 0, 1, 2)  # list widget goes in bottom-left
        layout.addWidget(self.plot, 0, 2, -1, -1)  # plot goes on right side, spanning
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 5)

    def update_list(self, x, y):
        self.plot.setList(x, y)
        self.listWidget.setList(x, y)

if __name__ == "__main__":
    options = argparse.ArgumentParser()
    options.add_argument("-f", "--file", type=str, required=False)
    args = options.parse_args()
    if not (fname := args.file):
        fname = "Code/QT/datavis/all_day.csv"
    #data = read_data(fname)
    app = QtWidgets.QApplication([])
    widget = MainWidget()
    window = MainWindow(widget)
    window.show()
    widget.update_list([1,2,3], [2,2,2])
    widget.update_list([1,2,3], [2,3,4])
    app.exec()

