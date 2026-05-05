from PySide6.QtWidgets import QPushButton, QLineEdit, QWidget, QListWidget, QGridLayout, QVBoxLayout, QMenu, QDialog
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QMouseEvent, QKeyEvent
from functools import partial
from time import sleep


class Form(QDialog):

    def __init__(self, value="", parent=None):
        super(Form, self).__init__(parent)
        self.edit = QLineEdit(value)
        self.button = QPushButton("OK")
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.close)


@Slot()
def edit_dialog(value):
    form = Form(value)
    form.setFixedSize(form.sizeHint())
    form.exec()
    return form.edit.text()


class ValList(QListWidget):
    def __init__(self, comSend, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.other_list: ValList = None
        self._comSend = comSend
    
    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        if (items := self.selectedItems()):
            edit_action = context_menu.addAction("Bearbeiten")
            edit_action.triggered.connect(lambda: partial(self._comSend,    2, self.selectedIndexes()[0], edit_dialog(items[0].text())))
            delete_action = context_menu.addAction("Löschen")
            delete_action.triggered.connect(lambda: partial(self._comSend,  1, self.selectedIndexes()[0]))
        context_menu.exec(event.globalPos())
    
    def mousePressEvent(self, event: QMouseEvent):
        if self.other_list == None:
            return super().mousePressEvent(event)
        self.other_list.clearSelection()
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
        self._comSend = comFunc
        self.__btn = QPushButton('Werte hinzufügen')
        self.__btn.clicked.connect(self.__onButtonClick)
        self.__textX = LineInput(placeholderText='X Wert')
        self.__textY = LineInput(placeholderText='Y Wert')
        self.__textX.on_enter = self.__onButtonClick
        self.__textY.on_enter = self.__onButtonClick
        self.__listX = ValList(comFunc)
        self.__listY = ValList(comFunc)
        self.__listX.other_list = self.__listY
        self.__listY.other_list = self.__listX
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
        self._comSend(0, valX, valY)

    def setList(self, x, y):
        for list_widget, elements in ((self.__listX, x), (self.__listY, y)):
            list_widget.clear()
            for item in elements:
                list_widget.addItem(str(item))