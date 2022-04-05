from PyQt5 import QtCore, QtGui
import sys
import os
from PyQt5.QtCore import  QEventLoop, QTimer ,Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QCheckBox, QPushButton, QWidget, QTableWidget, QHBoxLayout, QTableWidgetItem, QHeaderView
from execute import execute_fresh, execute_scan, execute_choose
from execute import *
from MainUI import Ui_MainWindow

# setor = [0, 0, 0, 0, 0, 0] #这个数组用来记录设置选择的内容
Whitelist = [0, 0, 0, 0]
Whitechoosen = [0, 0, 0, 0]
class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 500)
        self.setupUi(self)
        self.freshclam.clicked.connect(self.beginFresh)
        self.clamscan.clicked.connect(self.beginScan)
        self.choosefile.clicked.connect(self.beginChoose)
        self.whitelist.clicked.connect(self.beginWhite)
        self.setting.clicked.connect(self.beginSet)

    def beginFresh(self):
        execute_fresh()

    def beginScan(self):
        execute_scan()
    
    #扫描单个文件或者文件夹
    def beginChoose(self):
        items = ('选择文件扫描','选择文件夹扫描')
        item, ok = QInputDialog.getItem(self, "选择扫描", 'choose', items, 0, False)
        if ok and item:
            if item == '选择文件扫描':
                self.beginChoose1()
            else:
                self.beginChoose2()

    def beginChoose1(self):
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件')
        #a = 'clamscan'+' '+openfile_name[0]
        #print(a)
        #print(openfile_name[0])
        execute_choose(openfile_name[0])

    def beginChoose2(self):
        openfile_name = QFileDialog.getExistingDirectory(self, '选择文件夹')
        # a = 'clamscan'+' '+openfile_name
        # print(a)
        print(openfile_name)
        execute_choose(openfile_name)

    def beginWhite(self):
        self.set2 = WHITEWindow()
        self.set2.show()

    def beginSet(self):
        self.set1 = SETWindow()
        self.set1.show()

#设置界面布局（似乎不该写在这个文件里，后续调整）
class SETWindow(QWidget):
    global setor
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #新建6个复选框（参照clamtk）
        self.cb1 = QCheckBox("Scan for PUAs", self)
        self.cb2 = QCheckBox("Use heuristic scanning", self)
        self.cb3 = QCheckBox("Scan files beginning with a dot(.*)", self)
        self.cb4 = QCheckBox("Scan Files larger than 20 MB", self)
        self.cb5 = QCheckBox("Scan directories recursively", self)
        self.cb6 = QCheckBox("Check for updates to this program", self)

        bt = QPushButton('Back',self)

        self.resize(357, 507)
        self.setWindowTitle('设置')

        self.cb1.move(35, 30)
        self.cb2.move(35, 70)
        self.cb3.move(35, 110)
        self.cb4.move(35, 150)
        self.cb5.move(35, 190)
        self.cb6.move(35, 230)
        
        bt.move(130, 370)

        if setor[0] == 1:
            self.cb1.setChecked(True)
        if setor[1] == 1:
            self.cb2.setChecked(True)
        if setor[2] == 1:
            self.cb3.setChecked(True)
        if setor[3] == 1:
            self.cb4.setChecked(True)
        if setor[4] == 1:
            self.cb5.setChecked(True)
        if setor[5] == 1:
            self.cb6.setChecked(True)

        self.cb1.stateChanged.connect(self.changecb1)
        self.cb2.stateChanged.connect(self.changecb2)
        self.cb3.stateChanged.connect(self.changecb3)
        self.cb4.stateChanged.connect(self.changecb4)
        self.cb5.stateChanged.connect(self.changecb5)
        self.cb6.stateChanged.connect(self.changecb6)

        bt.clicked.connect(self.cls)

        self.show()

    def cls(self):
        self.close()
        for i in range(6):
            print(setor[i])

    def changecb1(self):
        if self.cb1.checkState() == Qt.Checked:
            setor[0] = 1
        elif self.cb1.checkState() == Qt.Unchecked:
            setor[0] = 0

    def changecb2(self):
        if self.cb2.checkState() == Qt.Checked:
            setor[1] = 1
        elif self.cb2.checkState() == Qt.Unchecked:
            setor[1] = 0

    def changecb3(self):
        if self.cb3.checkState() == Qt.Checked:
            setor[2] = 1
        elif self.cb3.checkState() == Qt.Unchecked:
            setor[2] = 0

    def changecb4(self):
        if self.cb4.checkState() == Qt.Checked:
            setor[3] = 1
        elif self.cb4.checkState() == Qt.Unchecked:
            setor[3] = 0

    def changecb5(self):
        if self.cb5.checkState() == Qt.Checked:
            setor[4] = 1
        elif self.cb5.checkState() == Qt.Unchecked:
            setor[4] = 0

    def changecb6(self):
        if self.cb6.checkState() == Qt.Checked:
            setor[5] = 1
        elif self.cb6.checkState() == Qt.Unchecked:
            setor[5] = 0

#白名单页面布局
class WHITEWindow(QWidget):
    currow = 0
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("白名单")
        self.resize(557, 507)
        conLayout = QHBoxLayout()
        tableWidget1 = QTableWidget()
        tableWidget1.setRowCount(4)
        tableWidget1.setColumnCount(1)
        conLayout.addWidget(tableWidget1)

        tableWidget1.setHorizontalHeaderLabels(['Directory'])
        tableWidget1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        for j in range(4):
            if Whitechoosen[j] == 1:
                tableWidget1.setItem(j, 0, QtWidgets.QTableWidgetItem(Whitelist[j]))


        add = QPushButton('添加文件', self)
        minus = QPushButton('移出文件', self)
        add.move(30, 320)
        minus.move(270, 320)

        conLayout.addWidget(add)
        conLayout.addWidget(minus)

        self.setLayout(conLayout)

        add.clicked.connect(lambda: self.add(tableWidget1))
        minus.clicked.connect(lambda: self.minus(tableWidget1))
        tableWidget1.clicked.connect(lambda: self.click(tableWidget1))

    def add(self, tableWidget):
        openfilename1 = QFileDialog.getExistingDirectory(self, '选择文件夹')
        
        cur = Whitechoosen[0] + Whitechoosen[1] + Whitechoosen[2] + Whitechoosen[3]
        tableWidget.setItem(cur, 0, QtWidgets.QTableWidgetItem(openfilename1))
        Whitelist[cur] = openfilename1
        Whitechoosen[cur] = 1

    def minus(self, tableWidget):
        #openfilename2 = QFileDialog.getExistingDirectory(self, '选择文件夹')
        #tableWidget.setItem(openfilename2)
        #global currow
        #tableWidget.removeRow(self.currow)
        #思路是首先修改Whitelist和 Whitechoosen
        #然后利用它们去重新构造tableWidget
        curtemp = self.currow
        cur = Whitechoosen[0] + Whitechoosen[1] + Whitechoosen[2] + Whitechoosen[3] - 1
        for i in range(4):
            if i == curtemp:
                if i < cur :
                    Whitelist[i] = Whitelist[i+1]
                    Whitechoosen[i] = 1
                    Whitechoosen[i+1] = 0
                    tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(Whitelist[i]))
                else :
                    Whitelist[i] = 0
                    Whitechoosen[i] = 0
                    tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(' '))
                curtemp = curtemp + 1

    def click(self, tableWidget):
        self.currow = tableWidget.currentRow()
        print(self.currow)




        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())