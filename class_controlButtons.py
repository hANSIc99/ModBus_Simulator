# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 19:31:53 2017

@author: Stephan
"""
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QToolTip, QPushButton, QMessageBox,
                             QDesktopWidget, QMainWindow, QAction, qApp,
                             QTextEdit, QLabel, QHBoxLayout, QVBoxLayout,
                             QGridLayout, QLineEdit, QLCDNumber, QSlider,
                             QInputDialog, QColorDialog, QFrame, QFontDialog,
                             QSizePolicy, QFileDialog, QCheckBox, QProgressBar,
                             QCalendarWidget, QSplitter, QComboBox)
from PyQt5.QtGui import QIcon, QFont, QColor, QPixmap, QPainter, QPen, QBrush
from PyQt5.QtCore import (QCoreApplication, Qt, QObject, pyqtSignal,
                          QBasicTimer, QDate, QPointF)

class controlButtons(QFrame):
    
    start_sig = pyqtSignal()
    reset_sig = pyqtSignal()
    
    def __init__(self):
        """ call the instructor of QWidget """
      
        super().__init__()
      
        """ call particular method """ 
        self.initUI() 
      
    def initUI(self):        
        """ set the variables inherited from QWidget """       
        print("initUI controlButtons")
        self.setMinimumSize(200, 150)
        self.setMaximumSize(200, 150)
        self.setFrameStyle(QFrame.Panel)
        """
        self.setStyleSheet("background-color: rgb(255, 200, 0)")
        """
        self.b_start = False
        
        self.btn1 = QPushButton('Start', self)
        self.btn1.clicked.connect(self.start_stop)
        self.btn1.move(15, 10)
        
        
        self.btn2 = QPushButton('Reset', self)
        self.btn2.clicked.connect(self.reset)
        self.btn2.move(105, 10)
        
        """
        self.paintEvent(self)
        """
        
    def start_stop(self):
        print("Start/Stop clicked")
        if self.b_start == False:    
            self.btn1.setText("Stop")
            self.b_start = True
        else:
            self.btn1.setText("Start")
            self.b_start = False
        self.start_sig.emit()

    def reset(self):
        print("reset clicked")
        self.reset_sig.emit()