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
from PyQt5.QtGui import (QIcon, QFont, QColor, QPixmap, QPainter, QPen, QBrush,
                         QDoubleValidator)
from PyQt5.QtCore import (QCoreApplication, Qt, QObject, pyqtSignal,
                          QBasicTimer, QDate, QPointF)

from PyQt5 import QtGui

class controlButtons(QFrame):
    
    start_sig = pyqtSignal()
    reset_sig = pyqtSignal()
    """
    Baustelle
    set_speed = pyqtSignal(QString)
    """
    
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
        
        """
        Buttons
        """
        
        self.btn1 = QPushButton('Start', self)
        self.btn1.clicked.connect(self.start_stop)
        self.btn1.move(15, 10)
        
        
        self.btn2 = QPushButton('Reset', self)
        self.btn2.clicked.connect(self.reset)
        self.btn2.move(105, 10)
        
        """
        Input Dialogs
        """
        lbl_pitch = QLabel('Pitch', self)
        lbl_pitch.move(15, 50)
        
        lbl_offs = QLabel('Offset', self)
        lbl_offs.move(105, 50)
        
        lbl_speed = QLabel('Speed', self)
        lbl_speed.move(15, 100)
        
        speed_box = QComboBox(self)
        speed_box.addItem("rad/s")
        speed_box.addItem("rpm")
        speed_box.addItem("Hz")
        speed_box.move(120, 120)
        
        self.le_pitch = QLineEdit(self)
        self.le_pitch.setMaximumWidth(70)
        self.le_pitch.move(15, 70)
        
        self.le_offs = QLineEdit(self)
        self.le_offs.setMaximumWidth(70)
        self.le_offs.move(105, 70)
        
        self.le_speed = QLineEdit(self)
        self.le_speed.setMaximumWidth(90)
        self.le_speed.move(15, 120)
        self.valid = QDoubleValidator(self)
        
        self.le_speed.setValidator(self.valid)
        """
        self.le_speed.textChanged.connect(self.speed_changed)
        """
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