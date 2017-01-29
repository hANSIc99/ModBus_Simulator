# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 18:08:51 2017

@author: Stephan
"""

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QToolTip, QPushButton, QMessageBox,
                             QDesktopWidget, QMainWindow, QAction, qApp,
                             QTextEdit, QLabel, QHBoxLayout, QVBoxLayout,
                             QGridLayout, QLineEdit, QLCDNumber, QSlider,
                             QInputDialog, QColorDialog, QFrame, QFontDialog,
                             QSizePolicy, QFileDialog, QCheckBox, QProgressBar,
                             QCalendarWidget, QSplitter, QComboBox, QBoxLayout)
from PyQt5.QtGui import (QIcon, QFont, QColor, QPixmap, QPainter, QPen, QBrush,
                         QDoubleValidator, QIntValidator)
from PyQt5.QtCore import (QCoreApplication, Qt, QObject, pyqtSignal,
                          QBasicTimer, QDate, QPointF)

from twisted.internet import reactor, protocol
from pymodbus.constants import Defaults

from pymodbus.client.async import ModbusClientProtocol
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.server.async import StartTcpServer, ModbusServerFactory

from pymodbus.transaction import ModbusSocketFramer

import logging
import datetime

from multiprocessing import Queue

from threading import Thread

from PyQt5 import QtGui

class ModBusClient(QFrame):
    
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    
    context = ModbusServerContext(slaves=None, single=True)
    
    register = 0
    slave_id = 0
    
    b_start = False
    
    def __init__(self):
      
        super().__init__()
      
        self.initUI() 
      
    def initUI(self): 
        
        f = QFont("Arial", 10, QFont.Bold)
        f2 = QFont("Arial", 8)
        
        valid_reg = QIntValidator(self)
        valid_reg.setRange(0, (2**16 - 4))
        
        valid_slave = QIntValidator(self)
        valid_slave.setRange(0, 2**8)
        
        
        
        lbl_0 = QLabel('Register Nr.:', self)
        lbl_0.move(5, 8)
        lbl_0.setFont(f)
        
        lbl_1 = QLabel('Slave ID:', self)
        lbl_1.move(5, 31)
        lbl_1.setFont(f)
        
        self.edit_reg = QLineEdit(self)
        self.edit_reg.move(100, 5)
        self.edit_reg.setMaximumWidth(70)
        self.edit_reg.setMaximumHeight(20)
        self.edit_reg.setText('0')
        self.edit_reg.setValidator(valid_reg)
        self.edit_reg.textChanged.connect(self.set_register)
        
        self.edit_slave = QLineEdit(self)
        self.edit_slave.move(100, 28)
        self.edit_slave.setMaximumWidth(70)
        self.edit_slave.setMaximumHeight(20)
        self.edit_slave.setText('0')
        self.edit_slave.setValidator(valid_slave)
        self.edit_slave.textChanged.connect(self.set_slave_ID)
        
        hbox_0 = QHBoxLayout()
        hbox_0.addWidget(lbl_0)
        
        hbox_1 = QHBoxLayout()
        hbox_1.addWidget(lbl_1)
        

        
        self.text_out = QTextEdit()
        self.text_out.setFont(f2)
        self.text_out.setReadOnly(True)
        self.text_out.setMinimumSize(50, 30)
        self.text_out.move(5, 100)

        
        layout = QVBoxLayout()
        layout.addLayout(hbox_0)
        layout.addLayout(hbox_1)
        layout.addWidget(self.text_out)
        layout.setSpacing(5)
        self.setLayout(layout)
        
        
        self.setMinimumSize(300, 150)
        self.setMaximumSize(300, 150)
        self.setFrameStyle(QFrame.Panel)
        
        print("ModBus Client initialized")
        
        
    def update_values(self, reg_0, reg_1, reg_2, reg_3):
        
        print("updating the context")
        
        function_code = 3
 
       
        values = [reg_0, reg_1, reg_2, reg_3]

        print("new values: " + str(values))
        self.context[self.slave_id].setValues(function_code, self.register, values)
        
        
    def client_stop(self):
        
        print("Client Stop activated")
        
        reactor.callFromThread(reactor.stop)
        
      
    def toggle_client(self):
        
        if self.b_start == False:
            
            print("Starting ModBus Client")
            """
            self.client_start()
            """
            self.b_start = True
            
        else:
            
            print("Stopping ModBus Client")
            """
            self.client_stop()
            """
            self.b_start = False
            
    
    def set_server(self, server):
        
       print("Server recieved")
       self.context = server   
       
    def set_register(self):
        
        try:
            self.register = int(self.edit_reg.text())
        except ValueError:
            self.log_message("Set a valid register number.")
        
    def set_slave_ID(self):
        
        try:
            self.slave_id = int(self.edit_slave.text())
        except ValueError:
            self.log_message("Set a valid slave ID.")
            
    def log_message(self, message):
        
        text = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : " + message)       
        self.text_out.append(text)
        
        
        

        
        
        
        