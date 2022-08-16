import pyqtgraph as pg
import numpy as np

app = pg.mkQApp()
x = np.random.normal(size=1000)
y = np.random.normal(size=1000)
pg.plot(x, y, pen=None, symbol='o')  # setting pen=None disables line drawing
# pg.QtGui.QGuiApplication.exec_()

a = pg.QtGui.QGuiApplication.exec()