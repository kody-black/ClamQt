#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from PyQt5.QtCore import  QEventLoop, QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QCheckBox, QPushButton, QWidget
 
from exeUI import Ui_Dialog

setor = [0, 0, 0, 0, 0, 0] #这个数组用来记录设置选择的内容
Whitelist = [0, 0, 0, 0]
Whitechoosen = [0, 0, 0, 0]

class EmittingStr(QtCore.QObject):
        textWritten = QtCore.pyqtSignal(str)  #定义一个发送str的信号
        def write(self, text):
            self.textWritten.emit(str(text))
            loop = QEventLoop()
            QTimer.singleShot(1000, loop.quit)
            loop.exec_()
 
class ControlBoard(QDialog, Ui_Dialog):
    def __init__(self):
        super(ControlBoard, self).__init__()
        self.setupUi(self)
        # 下面将输出重定向到textBrowser中
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
 
    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()
 
    def fresh(self):
        print('更新病毒库中\n请稍候......\n')
        d = os.popen("freshclam")
        f = d.read()
        print(f)
        print("更新完成!\n")
 
    def scan(self):
        print('病毒扫描中\n请稍候......\n')
        a = "clamscan"
        if setor[3]== 1:
            a = a+" "+"--max-filesize=20M"
            print(a)
        d = os.popen(a)
        f = d.read()
        print(f)
        print("扫描完成!\n")

        # --exclude-pua=CATEGORY
        #       Exclude a specific PUA category. This  option  can  be  used  multiple  times.
        #  --include-pua=CATEGORY
        #       Only  include  a specific PUA category. This option can be used multiple times.
        # --heuristic-scan-precedence[=yes/no(*)]
        #  --max-recursion=#n
        #       Set archive recursion level limit. This option protects  your  system  against  DoS
        #       attacks (default: 16).
        # --exclude=REGEX, --exclude-dir=REGEX
        #       Don't scan file/directory names matching regular expression. These options  can  be
        #       used multiple times.

    def choose(openfilename):
        print('病毒扫描中\n请稍候......\n')

        # --exclude-pua=CATEGORY
        #       Exclude a specific PUA category. This  option  can  be  used  multiple  times.
        #  --include-pua=CATEGORY
        #       Only  include  a specific PUA category. This option can be used multiple times.
        # --heuristic-scan-precedence[=yes/no(*)]
        #  --max-recursion=#n
        #       Set archive recursion level limit. This option protects  your  system  against  DoS
        #       attacks (default: 16).
        # --exclude=REGEX, --exclude-dir=REGEX
        #       Don't scan file/directory names matching regular expression. These options  can  be
        #       used multiple times.
        if setor[3]== 1:
            a = "clamscan"+" "+"--max-filesize=20M"+" "+openfilename
            print(a)
        else:
            a = "clamscan"+" "+openfilename
        d = os.popen(a)
        f = d.read()
        print(f)
        print("扫描完成!\n")
        


def execute_fresh():
    win = ControlBoard()
    win.setWindowTitle('病毒库更新')
    win.show()
    win.fresh()
    win.exec_()

def execute_scan():
    win = ControlBoard()
    win.setWindowTitle('病毒扫描')
    win.show()
    win.scan()
    win.exec_()

def execute_choose(openfilename):
    win = ControlBoard()
    win.setWindowTitle('选择文件扫描')
    win.show()
    win.choose(openfilename)
    win.exec_()

# def execute_set():
#     set1 = SETWindow()
#     # set1.exec()

# def openfile(self):
#     openfile_name = QFileDialog.getOpenFileName(self,'选择文件')