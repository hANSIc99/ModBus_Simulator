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
    
class DataClient(QWidget, Thread):
    
    """
    const (not changeable yet)
    timer_speed default value = 100
    """
    timer_speed = 500
    timer_step = 1 / 120
    offset = 0;
    pitch = 1;
    speed_opt = 0;
    speed_value = 0;
    speed_mode = ["rad/min", "rad/h", "1/min", "1/h", "1/day"]

    reg_0 = 0
    reg_1 = 0
    reg_2 = 0
    reg_3 = 0

    context = ModbusServerContext(slaves=None, single=True)
    
    
    
    def __init__(self):
        """ call the instructor of QWidget """
        super(DataClient, self).__init__()
        print("thats it")
        """ call particular method """ 
        
        self.initUI()
        
        
    def run(self):
        
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
        """
        connect log messages from controlButtons to arive here
        """
        
        self.buttons.log_message_sig.connect(self.log_message)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.buttons)
        hbox.addWidget(self.ptr)
        hbox.addWidget(self.modbus)
        hbox.addWidget(self.lcd)
        hbox.setAlignment(Qt.AlignLeft)
        hbox.setAlignment(Qt.AlignTop)
        
        self.buttons.start_sig.connect(self.toggleTimer)
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

        self.step = 0.0
        self.ptr.setValue(self.step)

        
    def timerEvent(self, e):
        
       
        if self.step >= 2* math.pi:
           self.step = 0
        
        self.step = self.step + self.timer_step
        """
        Thread(target=self.ptr.setValue, args=(self.step))
        """
        self.ptr.setValue(self.step)
        self.calc_value(self.step)


    def toggleTimer(self):
        
        
        if self.b_start == False:
            self.timer.start(self.timer_speed, self)
            self.log_message("Starting ModBus Client")
            self.log_message("Maximum Value: %0.2f" % (self.pitch + self.offset))
            self.log_message("Minimum Value: %0.2f" % ((-1) * self.pitch + self.offset))
            register = int(self.modbus.register)
            self.log_message("Values on register: %d - %d" % (register, register+3))
            
            self.b_start = True
        else:
            self.log_message("Stopping ModBus Client")
            self.timer.stop()
            self.b_start = False
            
    def set_speed(self, value, option):

        self.speed_opt = option
        self.speed_value = value
        if option == 0:
            
            """
            Value in rad/min
            """

            self.timer_step = value  /  120

        elif option == 1:
            
            """
            Value in rad/h
            """
            self.timer_step = value / 7200
            
        elif option == 2:
            """
            Value in rpm
            120 =^ 1 min (timer step = 500 ms)
            """
            self.timer_step = (math.pi * 2.0 * value  ) / 120

        elif option == 3:
            
            """
            Value in h^(-1)
            60 =^ 1 sec (timer step = 200 ms)
            """
            
            self.timer_step = (math.pi * 2.0 * value  ) / 7200

        elif option == 4:
            
            """
            Value in h^(-1)
            60 =^ 1 sec (timer step = 200 ms)
            """
            
            self.timer_step = (math.pi * 2.0 * value  ) / 172800

    def set_pitch(self, new_pitch):
        
        self.pitch = new_pitch
        
    def set_offset(self, new_offset):
        
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
        
        self.lcd.set_reg(self.reg_0, self.reg_1, self.reg_2, self.reg_3)
        """
        Thread(target=self.modbus.update_values, args=(self.reg_0, self.reg_1, self.reg_2, self.reg_3))
        """
        self.modbus.update_values(self.reg_0, self.reg_1, self.reg_2, self.reg_3)
        
    def log_message(self, message):
        
        self.modbus.log_message(message)
        
