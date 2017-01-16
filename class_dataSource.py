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

from class_pointer import PointerWidget
from class_controlButtons import controlButtons
from class_graph import graph



import sys, random, math
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
                          QBasicTimer, QDate, QPointF, pyqtSlot)




class Communicate(QObject):
    
    closeApp = pyqtSignal()
    
class Example(QWidget):
    
    def __init__(self):
        """ call the instructor of QWidget """
        super().__init__()
        """ call particular method """ 
        self.initUI()
        
    def initUI(self):        
        """ set the variables inherited from QWidget """ 
        
        """ Variables """
        
        self.b_start = False
        
        self.ptr = PointerWidget()     
        self.ptr.setValue(0.0)
        self.buttons = controlButtons()
        self.graph = graph()
        
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.buttons)
        hbox.addWidget(self.ptr)
        hbox.addWidget(self.graph)
        hbox.setAlignment(Qt.AlignLeft)
        hbox.setAlignment(Qt.AlignTop)
        
        self.buttons.start_sig.connect(self.toggleTimer)
        self.buttons.reset_sig.connect(self.resetTimer)
        
        self.setLayout(hbox)
        
        self.timer = QBasicTimer()
        self.step = 0.0
        """
        self.setGeometry(300, 300, 500, 500)
        """
        self.sizeHint()
        self.setWindowTitle('ModBus Simulator')
        self.setWindowIcon(QIcon('web.png'))
        self.show()
        

    def resetTimer(self):
        print("resetTimer clicked")
        self.step = 0.0
        self.ptr.setValue(self.step)

        
    def timerEvent(self, e):
        
       
        if self.step >= 2* math.pi:
           self.step = 0
        
        self.step = self.step + 0.01
        self.ptr.setValue(self.step)


    def toggleTimer(self):
        
        print("toggleTimer clicked")
        
        if self.b_start == False:
            self.timer.start(10, self)
            self.b_start = True
        else:
            self.timer.stop()
            self.b_start = False

    
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit", QMessageBox.Yes | 
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        

""" class inherits from QWidget """

    
  



if __name__ == '__main__':
    
    app = QApplication(sys.argv)
        
    ex = Example()
    
    sys.exit(app.exec_())