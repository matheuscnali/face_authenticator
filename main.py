import sys
import cv2
import random
import time
import matplotlib.pyplot as plt
from collections import deque
from PyQt5 import QtCore, QtGui, QtWidgets
from multiprocessing import Process

from view import Ui_MainWindow
from authenticator import Authenticator

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, source):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Create video capture.
        self.cap = cv2.VideoCapture(source)
        self.image = self.cap.read()[1]

        """ Image timer thread. """
        # Create a timer.
        self.timer_images = QtCore.QTimer(self)
        self.control_timer_images(delay=20)     

        # Set timer timeout callback function.
        self.timer_images.timeout.connect(self.update_cam_image)
    
    def get_image(self):
        return self.image

    def update_cam_image(self):

        # Read image in BGR format.
        _, image = self.cap.read()

        # Convert image to RGB format.
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Get image infos.
        height, width, channel = self.image.shape
        step = channel * width

        # Create QImage from image.
        qImg = QtGui.QImage(self.image.data, width, height, step, QtGui.QImage.Format_RGB888)

        # Show image in img_label.
        self.ui.img_cam_frontal.setPixmap(QtGui.QPixmap.fromImage(qImg))
        
    def control_timer_images(self, delay):

        if not self.timer_images.isActive():
            # Start timer.
            self.timer_images.start(delay)

        else:
            # Stop timer
            self.timer_images.stop()
            # Release video capture.
            self.cap.release()

class AuthenticatorThread(QtCore.QThread):

    def __init__(self, main_window):
        QtCore.QThread.__init__(self)
        self.authenticator = Authenticator()
        self.main_window = main_window

        self.main_window.ui.add_user.clicked.connect(self.add_user)
        self.main_window.ui.remove_user.clicked.connect(self.remove_user)

    def add_user(self):

        while True:
            #image = cv2.imread("example.jpeg")
            image = self.main_window.get_image()
            face_location = self.authenticator.face_crop(image)

            if face_location != []:
                top, right, bottom, left = face_location

                if self.authenticator.add_user(image[top:bottom, left:right], self.main_window.ui.id_text.toPlainText()):
                    break
            
            time.sleep(0.1)

    def remove_user(self):

        self.authenticator.remove_user(self.main_window.ui.id_text.toPlainText())


    def run(self):
        
        while True:
            
            #image = cv2.imread("example.jpeg")
            image = self.main_window.get_image()
            face_location = self.authenticator.face_crop(image)

            if face_location != []:
                top, right, bottom, left = face_location
                face = image[top:bottom, left:right]
                classification_result = self.authenticator.face_classifier(face)
            
                if classification_result[1]:
                    life_proof_result = self.authenticator.life_proof(face)
                    if life_proof_result:
                        self.main_window.ui.image_result.setVisible(True)
                        self.main_window.ui.text_result.setText("%s\nPassed in life proof." %(classification_result[0]))
                        self.main_window.ui.image_result.setPixmap(QtGui.QPixmap("data/gui_images/check.png"))
                    
                    else:
                        self.main_window.ui.image_result.setVisible(True)
                        self.main_window.ui.text_result.setText("%s\nFailed in life proof." %(classification_result[0]))
                        self.main_window.ui.image_result.setPixmap(QtGui.QPixmap("data/gui_images/alert.png"))

                elif classification_result[0] == "User does not exist in database.":
                    self.main_window.ui.image_result.setVisible(True)
                    self.main_window.ui.text_result.setText(classification_result[0])
                    self.main_window.ui.image_result.setPixmap(QtGui.QPixmap("data/gui_images/alert.png"))

            time.sleep(1)            
            self.main_window.ui.text_result.setText("")
            self.main_window.ui.image_result.setVisible(False)
    
              
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    # Create and show MainWindow.
    mainWindow = MainWindow(source=0)
    mainWindow.show()
    
    # Start authenticator thread.
    authenticator_thread = AuthenticatorThread(mainWindow)
    authenticator_thread.finished.connect(app.exit)
    authenticator_thread.start()

    sys.exit(app.exec_())
    
