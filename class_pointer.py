# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 19:30:35 2017

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
import sys, random, math

class PointerWidget(QFrame):
    
    def __init__(self):
        """ call the instructor of QWidget """
      
        super().__init__()
      
        """ call particular method """ 
        self.initUI()
        
    def initUI(self):        
        """ set the variables inherited from QWidget """       
        print("set pointer")
        self.bus_value = float()
        self.pointer = QPointF()
        self.start_point = QPointF(70.0, 70.0)
        
        self.setMinimumSize(150, 150)
        self.setMaximumSize(150, 150)
        self.setFrameStyle(QFrame.Panel)
        self.update()
        """
        self.paintEvent(self)
        """

    def setValue(self, value):
    
        new_x = math.cos(value) * 45 + self.start_point.x()
        new_y = math.sin(value) * -45 + self.start_point.y()
        self.bus_value = math.sin(value)
        self.pointer.setX(new_x)
        self.pointer.setY(new_y)
        self.update()
 

    def drawBrushes(self, qp):
        """
        print("drawBruches with x: %f, y: %f" % (self.pointer.x(), self.pointer.y()))
        """
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor('White'))
        qp.setBrush(brush)
        qp.drawEllipse(20, 20, 100, 100)
        pen = QPen(Qt.red, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(self.start_point, self.pointer)


        
    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)

        self.drawBrushes(qp)      
        qp.end()