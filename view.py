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
        MainWindow.resize(470, 550)
        icon = QtGui.QIcon()

        icon.addPixmap(QtGui.QPixmap("data/gui_images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.img_cam_frontal = QtWidgets.QLabel(self.centralwidget)
        self.img_cam_frontal.setGeometry(QtCore.QRect(10, 10, 450, 450))
        self.img_cam_frontal.setText("")
        self.img_cam_frontal.setPixmap(QtGui.QPixmap("data/gui_images/webcam.png"))
        self.img_cam_frontal.setScaledContents(True)
        self.img_cam_frontal.setObjectName("img_cam_frontal")

        self.image_result = QtWidgets.QLabel(self.centralwidget)
        self.image_result.setGeometry(QtCore.QRect(5, 490, 30, 30))
        self.image_result.setText("")
        self.image_result.setScaledContents(True)
        self.image_result.setObjectName("image_result")

        self.text_result = QtWidgets.QLabel(self.centralwidget)
        self.text_result.setGeometry(QtCore.QRect(40, 483, 451, 41))

        self.add_user = QtWidgets.QPushButton("Add user", self.centralwidget)
        self.add_user.setGeometry(QtCore.QRect(350, 490, 90, 32))
        self.add_user.setObjectName("add_user")

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
