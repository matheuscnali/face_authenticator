# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(490, 605)
        icon = QtGui.QIcon()

        icon.addPixmap(QtGui.QPixmap("data/gui_images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.cam_img = QtWidgets.QLabel(self.centralwidget)
        self.cam_img.setGeometry(QtCore.QRect(10, 10, 470, 470))
        self.cam_img.setText("")
        self.cam_img.setPixmap(QtGui.QPixmap("data/gui_images/webcam.png"))
        self.cam_img.setScaledContents(True)
        self.cam_img.setObjectName("img")

        self.img_result = QtWidgets.QLabel(self.centralwidget)
        self.img_result.setGeometry(QtCore.QRect(10, 545, 30, 30))
        self.img_result.setText("")
        self.img_result.setScaledContents(True)
        self.img_result.setObjectName("image_result")

        self.text_result = QtWidgets.QLabel(self.centralwidget)
        self.text_result.setGeometry(QtCore.QRect(50, 535, 451, 51))

        self.add_user = QtWidgets.QPushButton("Add user", self.centralwidget)
        self.add_user.setGeometry(QtCore.QRect(370, 495, 110, 38))
        self.add_user.setObjectName("add_user")

        self.remove_user = QtWidgets.QPushButton("Remove user", self.centralwidget)
        self.remove_user.setGeometry(QtCore.QRect(370, 545, 110, 38))
        self.remove_user.setObjectName("remove_user")

        self.id_text = QtWidgets.QTextEdit("", self.centralwidget)
        self.id_text.setGeometry(QtCore.QRect(10, 496, 350, 28))
        self.id_text.setObjectName("id_text")

        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(50)

        self.text_result.setFont(font)
        self.text_result.setObjectName("text_result")

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Face Authenticator"))
        self.text_result.setText(_translate("MainWindow", ""))
