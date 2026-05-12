from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon, QKeySequence
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, widget = None):
        super().__init__()
        self.setWindowTitle("PhysikDiagram")
        if widget:
            self.setCentralWidget(widget)
        # Menu
        self.__menu = self.menuBar()
        file_menu = self.__menu.addMenu("File")

        # Exit QAction
        file_menu.addAction(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit),
                            "Exit", QKeySequence.StandardKey.Quit, self.close)
        file_menu.addAction(QIcon.fromTheme(QIcon.ThemeIcon.DialogInformation),
                            "Info", QKeySequence.StandardKey.Print, self.info)

        # Status Bar
        self.__status = self.statusBar()
        self.__status.showMessage("App Running")
        QTimer.singleShot(1, self.__setSize)

    def __setSize(self):
        self.resize(self.sizeHint())

    def info(self):
        print(self.screen().orientation())