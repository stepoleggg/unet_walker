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
        mainWindow.resize(1035, 413)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.choseFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.choseFileButton.setGeometry(QtCore.QRect(20, 340, 131, 31))
        self.choseFileButton.setObjectName("choseFileButton")
        self.predictButton = QtWidgets.QPushButton(self.centralwidget)
        self.predictButton.setGeometry(QtCore.QRect(900, 50, 101, 31))
        self.predictButton.setObjectName("predictButton")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(500, 10, 391, 321))
        self.listWidget.setObjectName("listWidget")
        self.getDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.getDataButton.setGeometry(QtCore.QRect(900, 10, 101, 31))
        self.getDataButton.setObjectName("getDataButton")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 471, 321))
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setVisible(True)
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setGeometry(QtCore.QRect(340, 340, 131, 31))
        self.clearButton.setObjectName("clearButton")
        self.analyzeButton = QtWidgets.QPushButton(self.centralwidget)
        self.analyzeButton.setGeometry(QtCore.QRect(900, 90, 101, 31))
        self.analyzeButton.setObjectName("analyzeButton")
        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.editButton.setGeometry(QtCore.QRect(180, 340, 131, 31))
        self.editButton.setObjectName("editButton")
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
        self.analyzeButton.setText(_translate("mainWindow", "Анализ"))
        self.editButton.setText(_translate("mainWindow", "Настройки"))
