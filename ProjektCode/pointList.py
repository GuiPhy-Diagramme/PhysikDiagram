from PySide6.QtWidgets import QPushButton, QLineEdit, QWidget, QListWidget, QGridLayout, QListWidgetItem
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QMouseEvent


class ValList(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def mousePressEvent(self, event: QMouseEvent):
        print(event)
        print()



class PointList(QWidget):
    def __init__(self, comFunc, *args, **kargs):
        super().__init__(*args, *kargs)
        self._comSend = comFunc
        self.__btn = QPushButton('Werte hinzufügen')
        self.__btn.clicked.connect(self.__onButtonClick)
        self.__textX = QLineEdit(placeholderText='X Wert')
        self.__textY = QLineEdit(placeholderText="Y Wert")
        self.__listX = ValList()
        self.__listY = ValList()
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.__textX,   0, 0, 1, 1)
        layout.addWidget(self.__textY,   0, 1, 1, 1)
        layout.addWidget(self.__btn,     1, 0, 1, 2)
        layout.addWidget(self.__listX,   2, 0, 1, 1)
        layout.addWidget(self.__listY,   2, 1, 1, 1)
    
    def _stripVal(self, strVal: str) -> float | None:
        strVal = strVal.replace(',', '.')
        strVal.strip()
        try:
            return float(strVal)
        except ValueError:
            return None

    @Slot()
    def __onButtonClick(self):
        valX: float = self._stripVal(self.__textX.text())
        valY: float = self._stripVal(self.__textY.text())
        if type(valX) == None or type(valY) == None:
            return
        self._comSend(0, valX, valY)

    def setList(self, x, y):
        for list_widget, elements in ((self.__listX, x), (self.__listY, y)):
            list_widget.clear()
            for item in elements:
                list_widget.addItem(str(item))