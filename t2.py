import numpy as np
import pyqtgraph as pg
 
# 生成500*500矩阵的正态分布数据
data = np.random.normal(size=(500,500))
# 将数据显示为图片
pg.image(data, title="Simplest possible image example")
 
if __name__ == '__main__':
    pg.QtGui.QGuiApplication.exec_()
