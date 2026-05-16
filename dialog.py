import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(BASE_DIR, "libs")
sys.path.insert(0, LIBS_DIR)
from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QWidget
class Form(QDialog):
    def __init__(self, question, inputs = [("", "")], buttons = ["OK", "Abbrechen"], parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("PhysikDiagramm Dialog")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.question = QLabel(text=question)
        layout.addWidget(self.question)

        inputLayout = QHBoxLayout()
        self.inputs = [QLineEdit(vals[0], placeholderText=vals[1]) for vals in inputs]
        for inputField in self.inputs:
            inputLayout.addWidget(inputField)
        inputWidget = QWidget()
        inputWidget.setLayout(inputLayout)
        layout.addWidget(inputWidget)

        buttonsLayout = QHBoxLayout()
        self.buttons = [QPushButton(val) for val in buttons]
        for button in self.buttons:
            buttonsLayout.addWidget(button)
        buttonWidget = QWidget()
        buttonWidget.setLayout(buttonsLayout)
        layout.addWidget(buttonWidget)
        self.buttons[0].clicked.connect(self.accept)
        self.buttons[-1].clicked.connect(self.reject)
    