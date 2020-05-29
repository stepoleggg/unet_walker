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
        mainWindow.resize(458, 379)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.choseFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.choseFileButton.setGeometry(QtCore.QRect(10, 330, 131, 31))
        self.choseFileButton.setObjectName("choseFileButton")
        self.predictButton = QtWidgets.QPushButton(self.centralwidget)
        self.predictButton.setGeometry(QtCore.QRect(330, 90, 101, 31))
        self.predictButton.setObjectName("predictButton")
        self.trainButton = QtWidgets.QPushButton(self.centralwidget)
        self.trainButton.setGeometry(QtCore.QRect(330, 50, 101, 31))
        self.trainButton.setObjectName("trainButton")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 311, 311))
        self.listWidget.setObjectName("listWidget")
        self.getDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.getDataButton.setGeometry(QtCore.QRect(330, 10, 101, 31))
        self.getDataButton.setObjectName("getDataButton")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow"))
        self.choseFileButton.setText(_translate("mainWindow", "Выбрать файл"))
        self.predictButton.setText(_translate("mainWindow", "Предикт"))
        self.trainButton.setText(_translate("mainWindow", "Обучение"))
        self.getDataButton.setText(_translate("mainWindow", "Получить данные"))
