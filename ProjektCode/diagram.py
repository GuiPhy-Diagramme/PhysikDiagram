from pyqtgraph import PlotWidget


class Diagram(PlotWidget):
    def __init__(self, background = "default", *args, **kargs):
            pwArgList = ['title', 'labels', 'name', 'left', 'right', 'top', 'bottom', 'background']
            pwArgs = {}
            dataArgs = {}
            for k in kargs:
                if k in pwArgList:
                    pwArgs[k] = kargs[k]
                else:
                    dataArgs[k] = kargs[k]
            windowTitle = pwArgs.pop("title", "PlotWidget")
            super().__init__(**pwArgs)
            self.setWindowTitle(windowTitle)
            self.setBackground(background)
            self.showGrid(x = True, y = True)
    
    def draw(self, *args, **kwargs):
        self.plot(*args, symbol='o', **kwargs)

    def setList(self, x, y):
        self.clear()
        self.draw(x, y)