from PySide6 import QtWidgets
from mainWidget import MainWidget
from mainWindow import MainWindow
from collections import OrderedDict
from dialog import Form


class Controller:
    def __init__(self):
        self.__app = QtWidgets.QApplication([])
        self.__widget = MainWidget(self.comRecieve)
        self.__window = MainWindow(self.comRecieve, self.__widget)
        self.__window.show()
        self.__list = OrderedDict()
    
    def exec(self):
        self.__app.exec()
    
    def comRecieve(self, action, *args):
        if action == 0: # 0: Add Item
            print("Add Item", args)
            return self.addToList(args[0], args[1])
        if action == 1: # 1: Remove Item
            print("Remove Item", args)
            x = list(self.__list.keys())[args[0]]
            return self.removeFromList(x)
        if action == 2: # 2: Edit Item
            x = list(self.__list.keys())[args[0]]
            old = x, self.__list[x]
            dialog = Form("Neue Werte eingeben", [(str(old[0]), "x"), (str(old[1]), "y")])
            dialog.exec()
            if not dialog.result():
                return
            new_vals_str = dialog.inputs[0].text(), dialog.inputs[1].text()
            try:
                new_vals = float(new_vals_str[0]), float(new_vals_str[1])
            except ValueError:
                return
            self.removeFromList(x)
            return self.addToList(*new_vals)
        if action == 3: # Save
            print("Save File")
            pass

    def updateList(self):
        self.__widget.updateList(list(self.__list.keys()), list(self.__list.values()))

    def setList(self, x, y = None):
        if y is not None:
            x = zip(x, y)
        self.__list = OrderedDict(sorted(dict(x).items()))
        self.updateList()
    
    def addToList(self, x, y):
        self.__list[x] = y
        self.__list = OrderedDict(sorted(self.__list.items()))
        self.updateList()
    
    def removeFromList(self, x):
        out = x, self.__list.pop(x)
        self.updateList()
        return out


if __name__ == "__main__":
    controller = Controller()
    controller.exec()