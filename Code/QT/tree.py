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
    
    def readDir(self, path: QTreePathItem):
        pass


app = QApplication()
window = MainWindow()
app.exec()