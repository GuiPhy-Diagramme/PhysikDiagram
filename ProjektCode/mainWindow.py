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
        self._menu = self.menuBar()
        file_menu = self._menu.addMenu("File")

        # Exit QAction
        file_menu.addAction(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit),
                            "Exit", QKeySequence.StandardKey.Quit, self.close)
        file_menu.addAction(QIcon.fromTheme(QIcon.ThemeIcon.DialogInformation),
                            "Info", QKeySequence.StandardKey.Print, self.info)

        # Status Bar
        self._status = self.statusBar()
        self._status.showMessage("App Running")
        QTimer.singleShot(1, self._setSize)

    def _setSize(self):
        geometry = self.screen().availableGeometry()
        self.setBaseSize(geometry.width() * 0.8, geometry.height() * 0.7)

    def info(self):
        print(self.screen().orientation())