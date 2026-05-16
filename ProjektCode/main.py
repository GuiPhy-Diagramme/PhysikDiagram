from PySide6.QtWidgets import QApplication, QFileDialog
from mainWidget import MainWidget
from mainWindow import MainWindow
from collections import OrderedDict
from dialog import Form
from pathlib import Path
import json
from mathFunction import MathFunction


class Controller:
    def __init__(self):
        self.__app = QApplication([])
        self.__widget = MainWidget(self.comRecieve)
        self.__window = MainWindow(self.comRecieve, self.__widget)
        self.__window.show()
        self.__list = OrderedDict()
        self.__save_path = None
    
    def exec(self):
        self.__app.exec()
    
    def comRecieve(self, action, *args):
        if action == 0: # 0: Add Item
            return self.addToList(args[0], args[1])
        if action == 1: # 1: Remove Item
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
            if args[0]:
                return self.save_as()
            else:
                return self.save()
        if action == 4: # Load
            self.load()
        if action == 5:
            self.new()
        if action == 6:
            self.empty()
        if action == 7:
            self.use_func()
        if action == 8:
            self.differentiate()
        
    def use_func(self):
        dialog = Form("Function eingeben", inputs=[("-10", "Start"), ("10", "Ende"), ("0.2", "Schrittweite"), ("", "Funktion")])
        dialog.exec()
        if not dialog.result():
            return
        try:
            mfunc = MathFunction(dialog.inputs[3].text())
            i = float(dialog.inputs[0].text())
            e = float(dialog.inputs[1].text())
            s = float(dialog.inputs[2].text())
        except ValueError:
            return
        self.empty()
        while i <= e:
            i = round(i, 8)
            self.addToList(i, round(mfunc.calc(i), 8))
            i += s
            
    def differentiate(self):
        new_dict = {}
        x = list(self.__list.keys())
        y = list(self.__list.values())
        n = len(x)
        if n < 3:
            return
        # Anfang (Vorwärtsdifferenz 2. Ordnung)
        new_dict[x[0]] = (
            -3*y[0] + 4*y[1] - y[2]
        ) / (
            x[2] - x[0]
        )
        # Mitte (zentrale Differenz)
        for i in range(1, n - 1):

            new_dict[x[i]] = (
                y[i+1] - y[i-1]
            ) / (
                x[i+1] - x[i-1]
            )
        # Ende (Rückwärtsdifferenz 2. Ordnung)
        new_dict[x[-1]] = (
            3*y[-1] - 4*y[-2] + y[-3]
        ) / (
            x[-1] - x[-3]
        )
        self.setList(new_dict)

    def save_as(self):
        home = Path.home()
        fileName = QFileDialog.getSaveFileName(self.__window, "PhysikDiagramm — Datei Speichern als", str(home), "*.pdia")
        file_str = fileName[0].removesuffix(".pdia") + ".pdia"
        return self.save()
    
    def save(self):
        if self.__save_path == None:
            return save_as()
        save_json = json.dumps(self.__list)
        with open(self.__save_path, 'w') as f:
            f.write(save_json)
        self.set_save_path(self.__save_path)
    
    def new(self):
        self.set_save_path(None)
        self.empty()
    
    def empty(self):
        self.setList(dict())
    
    def load(self):
        home = Path.home()
        fileName = QFileDialog.getOpenFileName(self.__window, "Datei Öffnen", str(home), "*.pdia")
        with open(fileName[0], 'r') as f:
            load_json_str = f.read()
        load_json = json.loads(load_json_str)
        new_dict = dict()
        for item in load_json.items():
            try:
                new_dict[float(item[0])] = float(item[1])
            except ValueError:
                pass
        self.setList(new_dict)
        self.set_save_path(fileName[0])

    def updateList(self):
        self.__widget.updateList(list(self.__list.keys()), list(self.__list.values()))
        windowTitle = self.__window.windowTitle()
        if windowTitle[-2:] != " *":
            self.__window.setWindowTitle(windowTitle + " *")

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
    
    def set_save_path(self, new_path):
        self.__save_path = new_path
        title = "PhysikDiagramm"
        if new_path != None:
            title += " — " + new_path
        self.__window.setWindowTitle(title)


if __name__ == "__main__":
    controller = Controller()
    controller.exec()