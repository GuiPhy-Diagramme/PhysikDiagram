from PySide6.QtWidgets import QWidget, QMenu, QApplication
import sys

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create the context menu and add some actions
        self.context_menu = QMenu(self)
        action1 = self.context_menu.addAction("Action 1")
        action2 = self.context_menu.addAction("Action 2")
        action3 = self.context_menu.addAction("Action 3")

        # Connect the actions to methods
        action1.triggered.connect(self.action1_triggered)
        action2.triggered.connect(self.action2_triggered)
        action3.triggered.connect(self.action3_triggered)
        self.show()

    def contextMenuEvent(self, event):
        # Show the context menu
        self.context_menu.exec(event.globalPos())

    def action1_triggered(self):
        # Handle the "Action 1" action
        pass

    def action2_triggered(self):
        # Handle the "Action 2" action
        pass

    def action3_triggered(self):
        # Handle the "Action 3" action
        pass


app = QApplication(sys.argv)
window = MyWindow()
sys.exit(app.exec())