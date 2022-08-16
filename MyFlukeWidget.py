import sys


from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLineEdit, QApplication, QGridLayout

from pyqtgraph.Qt import QtGui, QtCore, QtWidgets


class MyFlukeWidget(QWidget):
    def __init__(self, parent=None):
        super(MyFlukeWidget, self).__init__(parent)
        self.resize(400, 300)
        layout = QtWidgets.QGridLayout()

        # 添加原生QWidget
        self.labelLogo = QtWidgets.QLabel()  # 注意QWidget() 内可以没有self!!
        self.labelLogo.setStyleSheet("background-color:grey;")

        self.pm = QPixmap("./img/vt650.jpeg")

        #self.labelLogo.setPixmap(self.pm)
        scaredPixmap = self.pm.scaled(100, 80, aspectRatioMode=Qt.KeepAspectRatio)
        self.labelLogo.setPixmap(scaredPixmap)
        self.labelLogo.setFixedSize(100, 80)

        self.combPort = QtWidgets.QComboBox()
        self.combPort.addItem('USB1')
        self.combPort.setFixedSize(100, 30)


        # 添加编辑框（QLineEdit）
        self.lineEdit = QtWidgets.QLineEdit("0")  # 注意QLineEdit("0") 内可以没self!!
        self.lineEdit.setFixedSize(100, 30)
        # 放入布局内
        layout.addWidget(self.labelLogo, 0, 0)
        layout.addWidget(self.combPort, 1, 0)
        layout.addWidget(self.lineEdit, 2, 0)
        self.setLayout(layout)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    fu = MyFlukeWidget()
    fu.show()
    sys.exit(app.exec_())
