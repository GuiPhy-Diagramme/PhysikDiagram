import sys
from PySide6.QtGui import QIcon, QKeySequence
from PySide6.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Earthquakes information")

        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("File")
        file_menu.addAction(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit), "Exit", QKeySequence.StandardKey.Quit, self.close)

        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")

        #geometry = self.screen().availableGeometry()
        #self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)
        
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()