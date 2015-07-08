# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/monitor.ui'
#
# Created: Wed Jul  8 15:00:53 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Monitor(object):
    def setupUi(self, Monitor):
        Monitor.setObjectName("Monitor")
        Monitor.resize(799, 576)
        self.verticalLayout = QtGui.QVBoxLayout(Monitor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.updateMonitorButton = QtGui.QPushButton(Monitor)
        self.updateMonitorButton.setObjectName("updateMonitorButton")
        self.horizontalLayout.addWidget(self.updateMonitorButton)
        self.host = QtGui.QLineEdit(Monitor)
        self.host.setObjectName("host")
        self.horizontalLayout.addWidget(self.host)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Monitor)
        QtCore.QMetaObject.connectSlotsByName(Monitor)

    def retranslateUi(self, Monitor):
        Monitor.setWindowTitle(QtGui.QApplication.translate("Monitor", "График RssPages", None, QtGui.QApplication.UnicodeUTF8))
        self.updateMonitorButton.setText(QtGui.QApplication.translate("Monitor", "Начать!", None, QtGui.QApplication.UnicodeUTF8))
        self.host.setInputMask(QtGui.QApplication.translate("Monitor", "000.000.000.000", None, QtGui.QApplication.UnicodeUTF8))

