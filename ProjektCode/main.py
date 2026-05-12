from PySide6 import QtWidgets
from mainWidget import MainWidget
from mainWindow import MainWindow
from collections import OrderedDict


class Controller:
    def __init__(self):
        self.__app = QtWidgets.QApplication([])
        self.__widget = MainWidget(self.comRecieve)
        self.__window = MainWindow(self.__widget)
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
            print("Edit Item", args)
            x = list(self.__list.keys())[args[1]]
            old = self.removeFromList(x)
            try:
                new_val = float(args[2])
            except ValueError:
                return
            if args[0]:
                new_item = new_val, old[1]
            else:
                new_item = x, new_val
            return self.addToList(*new_item)

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