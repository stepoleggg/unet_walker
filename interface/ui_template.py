# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setEnabled(True)
        mainWindow.resize(837, 518)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.choseFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.choseFileButton.setGeometry(QtCore.QRect(20, 340, 131, 31))
        self.choseFileButton.setObjectName("choseFileButton")
        self.predictButton = QtWidgets.QPushButton(self.centralwidget)
        self.predictButton.setGeometry(QtCore.QRect(700, 50, 101, 31))
        self.predictButton.setObjectName("predictButton")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(380, 10, 311, 321))
        self.listWidget.setObjectName("listWidget")
        self.getDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.getDataButton.setGeometry(QtCore.QRect(700, 10, 101, 31))
        self.getDataButton.setObjectName("getDataButton")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 361, 321))
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setVisible(True)
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setGeometry(QtCore.QRect(210, 340, 131, 31))
        self.clearButton.setObjectName("clearButton")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow"))
        self.choseFileButton.setText(_translate("mainWindow", "Выбрать файлы"))
        self.predictButton.setText(_translate("mainWindow", "Предикт"))
        self.getDataButton.setText(_translate("mainWindow", "Получить данные"))
        self.clearButton.setText(_translate("mainWindow", "Очистить"))
