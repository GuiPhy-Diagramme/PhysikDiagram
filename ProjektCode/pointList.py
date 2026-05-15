from PySide6.QtWidgets import QPushButton, QLineEdit, QWidget, QListWidget, QGridLayout, QMenu
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QMouseEvent, QKeyEvent
from functools import partial
from time import sleep

            delete_action.triggered.connect(self.delete_event)
        context_menu.exec(event.globalPos())
    
    def mousePressEvent(self, event: QMouseEvent):
        if self.__other_list == None:
            return super().mousePressEvent(event)
        self.__other_list.clearSelection()
        return super().mousePressEvent(event)


class LineInput(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_enter = None
    
    def keyPressEvent(self, arg__1: QKeyEvent):
        if arg__1.key() != Qt.Key.Key_Return:
            return super().keyPressEvent(arg__1)
        if self.on_enter == None:
            return
        self.on_enter()


class PointList(QWidget):
    def __init__(self, comFunc, *args, **kargs):
        super().__init__(*args, *kargs)
        self.comSend = comFunc
        self.__btn = QPushButton('Werte hinzufügen')
        self.__btn.clicked.connect(self.__onButtonClick)
        self.__textX = LineInput(placeholderText='X Wert')
        self.__textY = LineInput(placeholderText='Y Wert')
        self.__textX.on_enter = self.__onButtonClick
        self.__textY.on_enter = self.__onButtonClick
        self.__listX = ValList(comFunc, True)
        self.__listY = ValList(comFunc, False)
        self.__listX.__other_list = self.__listY
        self.__listY.__other_list = self.__listX
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
        if None in (valX, valY):
            return
        self.comSend(0, valX, valY)

    def setList(self, x, y):
        for list_widget, elements in ((self.__listX, x), (self.__listY, y)):
            list_widget.clear()
            for item in elements:
                list_widget.addItem(str(item))