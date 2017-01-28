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
from class_lcdnumber import Lcd
from class_ModBusClient import ModBusClient


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

from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from threading import Thread

class Communicate(QObject):
    
    closeApp = pyqtSignal()
    
class DataClient(QWidget):
    
    """
    const (not changeable yet)
    timer_speed default value = 100
    """
    timer_speed = 500;
    timer_step = 0.1;
    offset = 0;
    pitch = 1;
    speed_opt = 0;
    speed_value = 0;
    speed_mode = ["rad/min", "rpm", "Hz"]

    reg_0 = 0
    reg_1 = 0
    reg_2 = 0
    reg_3 = 0

    context = ModbusServerContext(slaves=None, single=True)
    
    
    
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
        self.modbus = ModBusClient()
        self.lcd = Lcd()
        
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.buttons)
        hbox.addWidget(self.ptr)
        hbox.addWidget(self.modbus)
        hbox.addWidget(self.lcd)
        hbox.setAlignment(Qt.AlignLeft)
        hbox.setAlignment(Qt.AlignTop)
        
        self.buttons.start_sig.connect(self.toggleTimer)
        self.buttons.start_sig.connect(self.modbus.toggle_client)
        self.buttons.reset_sig.connect(self.resetTimer)
        self.buttons.set_speed.connect(self.set_speed)
        self.buttons.set_offset.connect(self.set_offset)
        self.buttons.set_pitch.connect(self.set_pitch)
        
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
        
        self.step = self.step + self.timer_step
        self.ptr.setValue(self.step)
        self.calc_value(self.step)


    def toggleTimer(self):
        
        print("toggleTimer clicked")
        
        if self.b_start == False:
            self.timer.start(self.timer_speed, self)
            print("Start ModBus:\nOffset = " + str(self.offset))
            print("Pitch = " + str(self.pitch))
            print("Speed = " + str(self.speed_value) + " " + self.speed_mode[self.speed_opt])
            
            self.b_start = True
        else:
            self.timer.stop()
            self.b_start = False
            
    def set_speed(self, value, option):

        print("Set speed to " + str(value) + " option: " + str(option))
        self.speed_opt = option
        self.speed_value = value
        if option == 0:
            
            """
            Value in rad/min
            """

            self.timer_step = value / 300

        elif option == 1:
            """
            Value in rpm
            300 =^ 1 min (timer step = 200 ms)
            """
            self.timer_step = (math.pi * 2.0 * value  ) / 300

        elif option == 2:
            
            """
            Value in Hz
            60 =^ 1 sec (timer step = 200 ms)
            """
            
            self.timer_step = (2.0 * value  ) / 3

    def set_pitch(self, new_pitch):
        
        print("Set pitch to: " + str(new_pitch))
        self.pitch = new_pitch
        
    def set_offset(self, new_offset):
        
        print("Set offset to: " + str(new_offset))
        self.offset = new_offset
        
    def set_server(self, server):
        
        self.modbus.set_server(server)
        
    def calc_value(self, value):
        """
        Value = step value: max +/- 0.1
        """
        res_val = math.sin(value) * self.pitch
        res_val += self.offset
        
        high_word = int(res_val)
        
        self.reg_0 = high_word >> 16
        self.reg_1 = high_word & 0xffff
        """
        maximum value from decimals = 2^32
        """
        
        low_word = int((res_val % 1) * 1e9)
        
        
        self.reg_2 = low_word >> 16
        self.reg_3 = low_word & 0xffff
        
        
        
        print("low_word = " + str(low_word) + " reg_0 = " + str(self.reg_0) + " reg_1 = " + str(self.reg_1))
        
        self.lcd.set_reg(self.reg_0, self.reg_1, self.reg_2, self.reg_3)
        """
        Thread(target=self.modbus.update_values, args=(self.reg_0, self.reg_1, self.reg_2, self.reg_3))
        """
        self.modbus.update_values(self.reg_0, self.reg_1, self.reg_2, self.reg_3)
