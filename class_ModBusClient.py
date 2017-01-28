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
                             QCalendarWidget, QSplitter, QComboBox)
from PyQt5.QtGui import (QIcon, QFont, QColor, QPixmap, QPainter, QPen, QBrush,
                         QDoubleValidator)
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

from multiprocessing import Queue

from threading import Thread

from PyQt5 import QtGui

class ModBusClient(QFrame):
    
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    
    context = ModbusServerContext(slaves=None, single=True)
    
    b_start = False
    
    def __init__(self):
      
        super().__init__()
      
        self.initUI() 
      
    def initUI(self): 
        
        self.setMinimumSize(200, 150)
        self.setMaximumSize(200, 150)
        self.setFrameStyle(QFrame.Panel)
        
        print("ModBus Client initialized")
        
        
    def update_values(self, reg_0, reg_1, reg_2, reg_3):
        
        print("updating the context")
        
        
        function_code = 3
        slave_id = 0 
        address  = 0 
        """
        read values from register and 
        add one to it
        values = array

        values   = context[slave_id].getValues(register, address, count=5)
        values   = [v + 1 for v in values]
        """
        
        values = [reg_0, reg_1, reg_2, reg_3]
        """
        values = [88, 99, 77, 5, 6]
        """
        print("new values: " + str(values))
        self.context[slave_id].setValues(function_code, address, values)
        
        
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
        
        
        

        
        
        
        