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
        MainWindow.resize(800, 507)
        icon = QtGui.QIcon()

        icon.addPixmap(QtGui.QPixmap("data/gui_images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.img_cam_frontal = QtWidgets.QLabel(self.centralwidget)
        self.img_cam_frontal.setGeometry(QtCore.QRect(20, 20, 365, 365))
        self.img_cam_frontal.setText("")
        self.img_cam_frontal.setPixmap(QtGui.QPixmap("data/gui_images/webcam.png"))
        self.img_cam_frontal.setScaledContents(True)
        self.img_cam_frontal.setObjectName("img_cam_frontal")

        self.img_cam_side = QtWidgets.QLabel(self.centralwidget)
        self.img_cam_side.setGeometry(QtCore.QRect(415, 20, 365, 365))
        self.img_cam_side.setText("")
        self.img_cam_side.setPixmap(QtGui.QPixmap("data/gui_images/webcam.png"))
        self.img_cam_side.setScaledContents(True)
        self.img_cam_side.setObjectName("img_cam_side")

        self.image_result = QtWidgets.QLabel(self.centralwidget)
        self.image_result.setGeometry(QtCore.QRect(190, 420, 61, 61))
        self.image_result.setText("")
        self.image_result.setPixmap(QtGui.QPixmap("data/gui_images/check.png"))
        self.image_result.setScaledContents(True)
        self.image_result.setObjectName("image_result")
        self.text_result = QtWidgets.QLabel(self.centralwidget)
        self.text_result.setGeometry(QtCore.QRect(270, 430, 451, 41))

        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)

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
        self.text_result.setText(_translate("MainWindow", "TextLabel"))
