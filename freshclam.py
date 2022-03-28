#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
from PyQt5 import QtCore, QtGui
import sys
import os
from PyQt5.QtCore import  QEventLoop, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow,QDialog
 
from freshclamUI import Ui_Dialog
 
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
        d = os.popen("clamscan")
        f = d.read()
        print(f)
        print("扫描完成!\n")
     

def execute_fresh():
    win = ControlBoard()
    win.show()
    win.fresh()
    win.exec_()

def execute_scan():
    win = ControlBoard()
    win.setWindowTitle('病毒扫描')
    win.show()
    win.scan()
    win.exec_()