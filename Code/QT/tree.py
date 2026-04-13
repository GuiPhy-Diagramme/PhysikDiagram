import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QMainWindow

class QTreePathItem(QTreeWidgetItem):
    def __init__(self, strings, path: Path) -> None:
        super().__init__(strings)
        self.path = path

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Name", "Type"])
        self.setCentralWidget(self.tree)
        self.show()
        head = QTreePathItem([os.path.basename(cwd := Path.cwd()), "DICT"], cwd)
        self.tree.insertTopLevelItem(0, head)
        self.readDir(head)
    
    def readDir(self, head: QTreePathItem):
        to_do = []
        for item in head.path.iterdir():
            name = os.path.basename(item)
            ext = ""
            if item.is_dir():
                ext = "DICT"
            else:
                segments = name.split('.')
                if len(segments) > 1:
                    ext = segments[-1].upper()
            new_item = QTreePathItem([name, ext], item)
            head.addChild(new_item)
            if item.is_dir():
                to_do.append(new_item)
        for item in to_do:
            self.readDir(item)


app = QApplication()
window = MainWindow()
app.exec()