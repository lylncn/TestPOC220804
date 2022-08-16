import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QWidget, QVBoxLayout, QPushButton, QApplication, \
    QTreeWidgetItemIterator
from PyQt5.QtCore import Qt



class MyTestItemTree(QWidget):
    def __init__(self, QStringList=None):
        super().__init__()
        # 实例化一个树形结构，隐藏了header


        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(['项目', '状态'])
        self.tree.setColumnCount(2)
        self.tree.setColumnWidth(0, 150)
        # 顶级分支
        self.tree_main = QTreeWidgetItem(self.tree)
        self.tree_main.setText(0, 'POC')
        # 设置一些二级分支
        tree_second = ['呼吸压力', '气罐压力', '氧气', '机内温度', '适配器电压', '电池电压', '风扇', '阀门', '压缩机', '时钟', '存储器', '屏幕及按键', '氧气输出',
                       '理化指标', '电池', '噪声']
        self.gen_branch(self.tree_main, tree_second)
        # 设置一些三级分支
        tree_breathpress = ['精度测试', '准确度测试', '失效测试', '未检测呼吸报警测试']
        tree_gastankpress = ['精度测试', '准确度测试', '失效测试', '高压报警测试']
        tree_oxysensor = ['氧浓度精度', '氧浓度准确度', '流量精度', '流量准确度', '输出量', '通信故障', '氧浓度低报警']
        tree_temp = ['温度精度', '温度准确度', '传感器失效', '高温报警']
        tree_adaptervolage = ['精度', '准确度']
        tree_batteryvolage = ['精度', '准确度', '电池失效', '低电量']
        tree_fan  = ['转速精度', '风扇堵转或失效']
        tree_valve = ['常规时序', '睡眠时序', '阀门故障']
        tree_Compressor = ['反馈转速精度', '电机控制模拟量', '制动控制', '压缩机故障报警']
        tree_timeclock = ['时钟积累误差', '分子筛保养提醒']
        tree_storage = ['参数存储']
        tree_screentouch = ['按键测试', '屏幕测试', '灯光测试']
        tree_oxyout = ['输出最大压力', '脉冲触发灵敏度', '达氧时间', '氧气浓度', '1档脉冲流量', '2档脉冲流量', '3档脉冲流量', '4档脉冲流量', '5档脉冲流量', '5档脉冲流量', '连续气流流量']
        tree_physicschemistry = ['水分含量', '二氧化碳含量', '一氧化碳含量', '气态酸碱含量', "臭氧和其它气态氧化物含量", '气味', ' 固态物质含量', '固态物质颗粒']
        tree_battary = ['电池运行时间']
        tree_noise = ['噪声']


        self.gen_branch(self.tree_main.child(0), tree_breathpress)
        self.gen_branch(self.tree_main.child(1), tree_gastankpress)
        self.gen_branch(self.tree_main.child(2), tree_oxysensor)
        self.gen_branch(self.tree_main.child(3), tree_temp)
        self.gen_branch(self.tree_main.child(4), tree_adaptervolage)
        self.gen_branch(self.tree_main.child(5), tree_batteryvolage)
        self.gen_branch(self.tree_main.child(6), tree_fan)
        self.gen_branch(self.tree_main.child(7), tree_valve)
        self.gen_branch(self.tree_main.child(8), tree_Compressor)
        self.gen_branch(self.tree_main.child(9), tree_timeclock)
        self.gen_branch(self.tree_main.child(10), tree_storage)
        self.gen_branch(self.tree_main.child(11), tree_screentouch)
        self.gen_branch(self.tree_main.child(12), tree_oxyout)
        self.gen_branch(self.tree_main.child(13), tree_physicschemistry)
        self.gen_branch(self.tree_main.child(14), tree_battary)
        self.gen_branch(self.tree_main.child(15), tree_noise)
        '''
        item = QTreeWidgetItemIterator(self.tree)
        while item.value():
            if item.value().checkState(0) == QtCore.Qt.Checked:
                print(item.value())
                item = item.__iadd__(1)'''

        # 一个按钮
        self.pushButton = QPushButton('开始测试')
        self.pushButton.setFixedSize(200, 30)
        # 显示出来
        self.qvl = QVBoxLayout()
        self.qvl.addWidget(self.tree)
        self.qvl.addWidget(self.pushButton)
        self.setLayout(self.qvl)

        # 绑定一下槽函数，传入主要的分支节点
        self.pushButton.clicked.connect(lambda: self.get_checked(self.tree_main))

        self.tree.expandToDepth(1)

    @staticmethod
    def gen_branch(node: QTreeWidgetItem, texts: list):
        """ 给定某个节点和列表 在该节点生成列表内分支"""
        for text in texts:
            item = QTreeWidgetItem()
            item.setText(0, text)
            item.setCheckState(0, Qt.Unchecked)
            node.addChild(item)

    def get_checked(self, node: QTreeWidgetItem) -> list:
        """ 得到当前节点选中的所有分支， 返回一个 list """
        temp_list = []
        # 此处看下方注释 1
        for item in node.takeChildren():
            # 判断是否选中
            if item.checkState(0) == Qt.Checked:
                temp_list.append(item.text(0))
                # 判断是否还有子分支
                if item.childCount():
                    temp_list.extend(self.get_checked(item))
            node.addChild(item)
        print(temp_list)
        return temp_list


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyTestItemTree()
    win.show()
    sys.exit(app.exec_())
