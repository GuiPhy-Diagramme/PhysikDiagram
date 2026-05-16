import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(BASE_DIR, "libs")
sys.path.insert(0, LIBS_DIR)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon, QKeySequence
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, comFunc, widget = None):
        self.__comSend = comFunc
        super().__init__()
        self.setWindowTitle("PhysikDiagramm")
        if widget:
            self.setCentralWidget(widget)
        # Menu
        self.__menu = self.menuBar()
        file_menu = self.__menu.addMenu("Datei")
        edit_menu = self.__menu.addMenu("Bearbeiten")

        file_menu.addAction(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew),
                            "Neu", QKeySequence.StandardKey.New, self.new)
        file_menu.addAction(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen),
                            "Öffnen", QKeySequence.StandardKey.Open, self.load)
        file_menu.addAction(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave),
                            "Speichern", QKeySequence.StandardKey.Save, self.save)
        file_menu.addAction(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSaveAs),
                            "Speichern als", QKeySequence.StandardKey.SaveAs, self.save_as)
        file_menu.addAction(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit),
                            "Beenden", QKeySequence.StandardKey.Quit, self.close)
        
        edit_menu.addAction(QIcon.fromTheme(QIcon.ThemeIcon.EditClear),
                            "Leeren", self.empty)
        edit_menu.addAction("Funktion eingeben", self.math_function)
        edit_menu.addAction("Ableiten", self.differentiate)
        edit_menu.addAction("Integrieren", self.integrate)
        edit_menu.addAction("Verschieben", self.move)
        edit_menu.addAction("Strecken/Stauchen", self.stretch)
        edit_menu.addAction("Auflösung verändern", self.scale)

        self.__status = self.statusBar()
        self.__status.showMessage("App läuft")
        QTimer.singleShot(1, self.__setSize)

    def __setSize(self):
        self.resize(self.sizeHint())
    
    def new(self):
        self.__comSend(5)
    
    def load(self):
        self.__comSend(4)

    def save_as(self):
        self.__comSend(3, 1)

    def save(self):
        self.__comSend(3, 0)
    
    def empty(self):
        self.__comSend(6)
    
    def math_function(self):
        self.__comSend(7)
    
    def differentiate(self):
        self.__comSend(8)
    
    def integrate(self):
        self.__comSend(9)
    
    def move(self):
        self.__comSend(10)
    
    def stretch(self):
        self.__comSend(11)
    
    def scale(self):
        self.__comSend(12)