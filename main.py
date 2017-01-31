# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 08:52:22 2017

@author: Stephan


pymodbus.datastore.context.py edited
pymodbus.server.async.py edited

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
from twisted.internet import reactor, protocol, defer
from threading import Thread
from pymodbus.transaction import ModbusSocketFramer
from pymodbus.server.async import StartTcpServer, ModbusServerFactory
from pymodbus.datastore import ModbusSequentialDataBlock
import atexit


class Main(QWidget): 
    
    log_message_sig = pyqtSignal(str)
    
    def __init__(self):

        super().__init__()

        self.initServer()      
        self.initUI()            
        self.log_message_sig.connect(self.data_1.log_message)
        

        
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
        """
        construction site: mutliple data sources and log windows must be possible
        """
        store.callback_log(self.log_message)
        
        self.context = ModbusServerContext(slaves=store, single=True)

        address = "", Defaults.Port
        framer  = ModbusSocketFramer
        factory = ModbusServerFactory(self.context, framer, identity=None)                
        
        reactor.listenTCP(address[1], factory, interface=address[0])                
        
        Thread(target=reactor.run).start()
        
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit", QMessageBox.Yes | 
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            reactor.callFromThread(reactor.stop)
            event.accept()
        else:
            event.ignore()
            
    def log_message(self, message):
        
        self.log_message_sig.emit(message)

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    ex = Main()
    
    sys.exit(app.exec_())
