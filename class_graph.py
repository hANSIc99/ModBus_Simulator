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

class graph(QFrame):
    

    
    def __init__(self):
        """ call the instructor of QWidget """
      
        super().__init__()
      
        """ call particular method """ 
        self.initUI() 
      
    def initUI(self):        
        """ set the variables inherited from QWidget """       
        print("initUI Frames")
        self.setMinimumSize(500, 150)
        self.setMaximumSize(500, 150)
        self.setFrameStyle(QFrame.Panel)
