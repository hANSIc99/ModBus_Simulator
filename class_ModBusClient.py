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
from pymodbus.server.async import StartTcpServer
import logging

from PyQt5 import QtGui

class ModBusClient(QFrame):
    
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    
    def __init__(self):
        """ call the instructor of QWidget """
      
        super().__init__()
      
        """ call particular method """ 
        self.initUI() 
      
    def initUI(self): 
        
        self.setMinimumSize(200, 150)
        self.setMaximumSize(200, 150)
        self.setFrameStyle(QFrame.Panel)
       
        store = ModbusSlaveContext(
            di = ModbusSequentialDataBlock(0, [17]*100),
            co = ModbusSequentialDataBlock(0, [17]*100),
            """"hr = holding register"""
            hr = ModbusSequentialDataBlock(0, [17]*100),
            ir = ModbusSequentialDataBlock(0, [17]*100))
        
        context = ModbusServerContext(slaves=store, single=True)
        

       
        StartTcpServer(context)
        
        
        print("ModBus Client initialized")
    """     
    def dassert(deferred, callback):
        def _assertor(value, message=None):
            assert value, message
            deferred.addCallback(lambda r: _assertor(callback(r)))
            deferred.addErrback(lambda  e: _assertor(False, e))
    """
    def process(client):
        result = client.write_coil(1, True)
        result.addCallback(printResult)
        reactor.callLater(1, reactor.stop)
        
        
    def printResult(result):
        print("Result: %d" % result.bits[0])
        
        
        
        
        