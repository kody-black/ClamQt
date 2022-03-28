from PyQt5 import QtCore, QtGui
import sys
import os
from PyQt5.QtCore import  QEventLoop, QTimer ,Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from freshclam import execute_fresh,execute_scan
 
from MainUI import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 500)
        self.setupUi(self)
        self.freshclam.clicked.connect(self.beginFresh)
        self.clamscan.clicked.connect(self.beginScan)

    def beginFresh(self):
        execute_fresh()

    def beginScan(self):
        execute_scan()
        
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())