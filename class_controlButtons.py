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
    
    log_message_sig = pyqtSignal(str)
    
    set_speed   =    pyqtSignal(float, int)
    set_offset  =    pyqtSignal(float)
    set_pitch   =    pyqtSignal(float)
    
    options = ["rad/min", "rad/h", "1/min", "1/h", "1/day"]
    
    
    def __init__(self):
        """ call the instructor of QWidget """
      
        super().__init__()
      
        """ call particular method """ 
        self.initUI() 
      
    def initUI(self):        
        """ set the variables inherited from QWidget """       
        
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
        
        """
        the validator is valid for all QLineEdit's
        """
        self.valid = QDoubleValidator(self)
        
        self.speed_box = QComboBox(self)
        self.speed_box.addItem(self.options[0])
        self.speed_box.addItem(self.options[1])
        self.speed_box.addItem(self.options[2])
        self.speed_box.addItem(self.options[3])
        self.speed_box.addItem(self.options[4])
        self.speed_box.move(120, 120)
        """
        Connect speed_box to speed_changed to trigger an update
        """
        self.speed_box.currentIndexChanged.connect(self.speed_changed)
        
        self.le_pitch = QLineEdit(self)
        self.le_pitch.setMaximumWidth(70)
        self.le_pitch.move(15, 70)
        self.le_pitch.setValidator(self.valid)
        self.le_pitch.setText("1")
        
        self.le_offs = QLineEdit(self)
        self.le_offs.setMaximumWidth(70)
        self.le_offs.move(105, 70)
        self.le_offs.setValidator(self.valid)
        self.le_offs.setText("0")
        
        self.le_speed = QLineEdit(self)
        self.le_speed.setMaximumWidth(90)
        self.le_speed.move(15, 120)               
        self.le_speed.setValidator(self.valid)
        self.le_speed.setText("1")
        
        self.le_speed.textChanged[str].connect(self.speed_changed)
        self.le_offs.textChanged[str].connect(self.offset_changed)
        self.le_pitch.textChanged[str].connect(self.pitch_changed)
        
       
    def speed_changed(self):
        
        try:
            result = float(self.le_speed.text())
            option = self.speed_box.currentIndex()
            self.log_message_sig.emit("Speed changed: %0.2f %s" % (result, self.options[option]))
            self.set_speed.emit(result, option)
        except ValueError:
            self.log_message_sig.emit("Invalid speed value")
            
    def offset_changed(self):
        
        try:
            result = float(self.le_offs.text())
            self.set_offset.emit(result)
            self.log_message_sig.emit("Offset changed: %0.2f" % result)
        except ValueError:
            self.log_message_sig.emit("Invalid offset value")           
        
    def pitch_changed(self):        
        try:
            result = float(self.le_pitch.text())
            self.set_pitch.emit(result)
            self.log_message_sig.emit("Pitch changed: %0.2f" % result)
        except ValueError:
            self.log_message_sig.emit("Invalid pitch value")
        
    def start_stop(self):
        
        if self.b_start == False:    
            self.btn1.setText("Stop")
            self.b_start = True
        else:
            self.btn1.setText("Start")
            self.b_start = False
        self.start_sig.emit()

    def reset(self):
        
        self.log_message_sig.emit("Timer reset")
        self.reset_sig.emit()
