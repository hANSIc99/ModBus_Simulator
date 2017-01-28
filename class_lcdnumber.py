# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 09:18:48 2017

@author: Stephan
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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

class Lcd(QFrame):
    

    
    def __init__(self):
        """ call the instructor of QWidget """
      
        super().__init__()
      
        """ call particular method """ 
        self.initUI() 
      
    def initUI(self):        
        """ set the variables inherited from QWidget """       
        print("initUI Frames")
        self.setMinimumSize(200, 150)
        self.setMaximumSize(200, 150)
        self.setFrameStyle(QFrame.Panel)
        
        self.reg_0 = QLCDNumber(self)
        self.reg_0.resize(140, 30)
        self.reg_0.move(50, 6)       
        self.reg_0.setNumDigits(5)
        self.reg_0.segmentStyle = QLCDNumber.Flat

        self.reg_1 = QLCDNumber(self)
        self.reg_1.resize(140, 30)
        self.reg_1.move(50, 42)       
        self.reg_1.setNumDigits(5)
        
        self.reg_2 = QLCDNumber(self)
        self.reg_2.resize(140, 30)
        self.reg_2.move(50, 78)       
        self.reg_2.setNumDigits(5)
        
        self.reg_3 = QLCDNumber(self)
        self.reg_3.resize(140, 30)
        self.reg_3.move(50, 114)       
        self.reg_3.setNumDigits(5)
        
    def set_reg(self, reg_0, reg_1, reg_2, reg_3):
        
        self.reg_0.display(reg_0)
        self.reg_1.display(reg_1)
        self.reg_2.display(reg_2)
        self.reg_3.display(reg_3)
        
        
        
