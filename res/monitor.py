# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/monitor.ui'
#
# Created: Thu Jul  9 08:55:43 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_HotAutumn(object):
    def setupUi(self, HotAutumn):
        HotAutumn.setObjectName("HotAutumn")
        HotAutumn.resize(799, 576)
        self.verticalLayout = QtGui.QVBoxLayout(HotAutumn)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.updateMonitorButton = QtGui.QPushButton(HotAutumn)
        self.updateMonitorButton.setObjectName("updateMonitorButton")
        self.horizontalLayout.addWidget(self.updateMonitorButton)
        self.host = QtGui.QLineEdit(HotAutumn)
        self.host.setObjectName("host")
        self.horizontalLayout.addWidget(self.host)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(HotAutumn)
        QtCore.QMetaObject.connectSlotsByName(HotAutumn)

    def retranslateUi(self, HotAutumn):
        HotAutumn.setWindowTitle(QtGui.QApplication.translate("HotAutumn", "Hot Autumn", None, QtGui.QApplication.UnicodeUTF8))
        self.updateMonitorButton.setText(QtGui.QApplication.translate("HotAutumn", "Начать!", None, QtGui.QApplication.UnicodeUTF8))
        self.host.setInputMask(QtGui.QApplication.translate("HotAutumn", "000.000.000.000", None, QtGui.QApplication.UnicodeUTF8))

