# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EventHandel.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(748, 445)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.makePWButton = QtWidgets.QPushButton(self.centralwidget)
        self.makePWButton.setGeometry(QtCore.QRect(300, 330, 161, 71))
        self.makePWButton.setObjectName("makePWButton")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(40, 240, 161, 71))
        self.startButton.setObjectName("startButton")
        self.extractDBBtn = QtWidgets.QPushButton(self.centralwidget)
        self.extractDBBtn.setGeometry(QtCore.QRect(550, 240, 161, 71))
        self.extractDBBtn.setObjectName("extractDBBtn")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(40, 330, 161, 71))
        self.stopButton.setObjectName("stopButton")
        self.restoreDBBtn = QtWidgets.QPushButton(self.centralwidget)
        self.restoreDBBtn.setGeometry(QtCore.QRect(550, 330, 161, 71))
        self.restoreDBBtn.setObjectName("restoreDBBtn")
        self.extractDBBtn2xlsx = QtWidgets.QPushButton(self.centralwidget)
        self.extractDBBtn2xlsx.setGeometry(QtCore.QRect(550, 150, 161, 71))
        self.extractDBBtn2xlsx.setObjectName("extractDBBtn2xlsx")
        self.portText = QtWidgets.QLineEdit(self.centralwidget)
        self.portText.setGeometry(QtCore.QRect(40, 170, 161, 31))
        self.portText.setObjectName("portText")
        self.portBtn = QtWidgets.QPushButton(self.centralwidget)
        self.portBtn.setGeometry(QtCore.QRect(210, 170, 131, 31))
        self.portBtn.setObjectName("portBtn")

        self.timerText = QtWidgets.QLineEdit(self.centralwidget)
        self.timerText.setGeometry(QtCore.QRect(40, 100, 161, 31))
        self.timerText.setObjectName("timerText")
        self.timerBtn = QtWidgets.QPushButton(self.centralwidget)
        self.timerBtn.setGeometry(QtCore.QRect(210, 100, 171, 31))
        self.timerBtn.setObjectName("timerBtn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.makePWButton.setText(_translate("MainWindow", "產生帳號密碼"))
        self.startButton.setText(_translate("MainWindow", "啟動伺服器"))
        self.extractDBBtn.setText(_translate("MainWindow", "抽取資料庫"))
        self.stopButton.setText(_translate("MainWindow", "停止伺服器"))
        self.restoreDBBtn.setText(_translate("MainWindow", "載入備份資料集"))
        self.extractDBBtn2xlsx.setText(_translate("MainWindow", "抽取資料庫到xlsx"))
        self.portBtn.setText(_translate("MainWindow", "設定連接埠(port)"))
        self.timerBtn.setText(_translate("MainWindow", "設定每題作答時間(sec)"))


