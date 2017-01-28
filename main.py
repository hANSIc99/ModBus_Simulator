# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 08:52:22 2017

@author: Stephan
"""

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

from class_dataSource import DataClient
from pymodbus.constants import Defaults
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from twisted.internet import reactor, protocol
from threading import Thread
from pymodbus.transaction import ModbusSocketFramer
from pymodbus.server.async import StartTcpServer, ModbusServerFactory
from pymodbus.datastore import ModbusSequentialDataBlock
import atexit

class Main(QWidget): 
    
    
    
    def __init__(self):

        super().__init__()
        self.initServer()
        self.initUI()
        
        
    def initUI(self):        
        
        self.data_1 = DataClient()
        self.data_1.set_server(self.context)
        vbox = QVBoxLayout()
        vbox.addWidget(self.data_1)
        
        

        self.setLayout(vbox)
        self.sizeHint()
        self.setWindowTitle('ModBus Simulator')
        self.setWindowIcon(QIcon('web.png'))
        self.show()
        
    def initServer(self):
        
        print("class_ModBus Start clicked")
        store = ModbusSlaveContext(
            di = ModbusSequentialDataBlock(0, [17]*100),
            co = ModbusSequentialDataBlock(0, [17]*100),    
            hr = ModbusSequentialDataBlock(0, [17]*100),
            ir = ModbusSequentialDataBlock(0, [17]*100))
        
        self.context = ModbusServerContext(slaves=store, single=True)

        address = "", Defaults.Port
        framer  = ModbusSocketFramer
        factory = ModbusServerFactory(self.context, framer, identity=None)
        reactor.listenTCP(address[1], factory, interface=address[0])
        Thread(target=reactor.run).start()

        print("Starting Modbus TCP Server on %s:%s" % address)
        
        
    def closeEvent(self, event):
        
        reactor.callFromThread(reactor.stop)
        
        print("closing")
        
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
        
    ex = Main()
    
    sys.exit(app.exec_())