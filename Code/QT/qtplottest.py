import sys
import argparse
import pandas as pd
import pyqtgraph as pg
import time
from dateutil import parser
from PySide6.QtGui import QIcon, QKeySequence
from PySide6.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("Eartquakes information")
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
            #self.show()


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


if __name__ == "__main__":
    options = argparse.ArgumentParser()
    options.add_argument("-f", "--file", type=str, required=True)
    args = options.parse_args()
    data = read_data(args.file)
    print(data)
    app = QApplication()
    window = MainWindow(Diagramm(*data))
    window.show()
    app.exec()
    
    