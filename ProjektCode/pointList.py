from PySide6.QtWidgets import QPushButton, QLineEdit, QWidget, QListWidget, QGridLayout, QVBoxLayout, QMenu, QDialog
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QMouseEvent, QKeyEvent
from PySide6.QtGui import QMouseEvent
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
    form.exec()
    return form.edit.text()


class ValList(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.other_list: ValList = None
    
    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        context_menu.addAction("test")
        if (items := self.selectedItems()):
            edit_action = context_menu.addAction("Bearbeiten")
            edit_action.triggered.connect(lambda: items[0].setText(edit_dialog(items[0].text())))
        context_menu.exec(event.globalPos())
    
    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        self.other_list.clearSelection()


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
        self.__textX = QLineEdit(placeholderText='X Wert')
        self.__textY = QLineEdit(placeholderText='Y Wert')
        self.__listX = ValList()
        self.__listY = ValList()
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
        if type(valX) == None or type(valY) == None:
            return
        self._comSend(0, valX, valY)

    def setList(self, x, y):
        for list_widget, elements in ((self.__listX, x), (self.__listY, y)):
            list_widget.clear()
            for item in elements:
                list_widget.addItem(str(item))