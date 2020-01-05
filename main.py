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

    def __init__(self, img_source):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Create video capture
        self.cap = cv2.VideoCapture(img_source)
        self.cam_img = self.cap.read()[1]

        # Create a timer to update camera image in GUI
        self.img_timer = QtCore.QTimer(self)
        self.img_timer_control(delay=20)     

        # Set timer timeout callback function
        self.img_timer.timeout.connect(self.update_cam_img)
    
    def get_cam_img(self):
        return self.cam_img

    def update_cam_img(self):

        # Read image in BGR format
        self.cam_img = self.cap.read()[1]

        # Convert image to RGB format
        self.cam_img = cv2.cvtColor(self.cam_img, cv2.COLOR_BGR2RGB)

        # Get image infos
        height, width, channel = self.cam_img.shape
        step = channel * width

        # Create QImage from image
        qImg = QtGui.QImage(self.cam_img.data, width, height, step, QtGui.QImage.Format_RGB888)

        # Show image in img_label
        self.ui.cam_img.setPixmap(QtGui.QPixmap.fromImage(qImg))
        
    def img_timer_control(self, delay):

        if not self.img_timer.isActive():
            # Start timer
            self.img_timer.start(delay)

        else:
            # Stop timer
            self.img_timer.stop()
            # Release video capture
            self.cap.release()

class AuthenticatorThread(QtCore.QThread):

    def __init__(self, main_window):
        QtCore.QThread.__init__(self)
        self.authenticator = Authenticator()
        self.main_window = main_window
        
        # Create a link between buttons and functions
        self.main_window.ui.add_user.clicked.connect(self.add_user)
        self.main_window.ui.remove_user.clicked.connect(self.remove_user)

    def add_user(self):

        image = self.main_window.get_cam_img()
        face_location = self.authenticator.face_crop(image)

        if face_location:
            top, right, bottom, left = face_location
            
            try:
                face = image[top:bottom, left:right]
                self.authenticator.add_user(face, self.main_window.ui.id_text.toPlainText())
            except:
                self.main_window.ui.text_result.setText("Face not detected!")
                self.main_window.ui.img_result.setVisible(True)
                self.main_window.ui.img_result.setPixmap(QtGui.QPixmap("data/gui_images/alert.png"))
                return

        else:
            self.main_window.ui.text_result.setText("Face not detected!")
            self.main_window.ui.img_result.setVisible(True)
            self.main_window.ui.img_result.setPixmap(QtGui.QPixmap("data/gui_images/alert.png"))

    def remove_user(self):

        self.authenticator.remove_user(self.main_window.ui.id_text.toPlainText())

    def run(self):
        
        while True:
            cam_img = self.main_window.get_cam_img()
            face_location = self.authenticator.face_crop(cam_img)

            if face_location:
                top, right, bottom, left = face_location
                face = cam_img[top:bottom, left:right]

                classification_result = self.authenticator.face_classifier(face)

                if classification_result:
                    life_proof_result = self.authenticator.life_proof(face, debug=True)
                    if life_proof_result:
                        self.main_window.ui.text_result.setText("%s\nPassed in life proof." %(classification_result))
                        self.main_window.ui.img_result.setVisible(True)
                        self.main_window.ui.img_result.setPixmap(QtGui.QPixmap("data/gui_images/check.png"))
                    
                    else:
                        self.main_window.ui.text_result.setText("%s\nFailed in life proof." %(classification_result))
                        self.main_window.ui.img_result.setVisible(True)
                        self.main_window.ui.img_result.setPixmap(QtGui.QPixmap("data/gui_images/alert.png"))

                else:
                    self.main_window.ui.text_result.setText("User does not exist in database.")
                    self.main_window.ui.img_result.setVisible(True)
                    self.main_window.ui.img_result.setPixmap(QtGui.QPixmap("data/gui_images/alert.png"))

            time.sleep(1)            
            self.main_window.ui.img_result.setVisible(False)
            self.main_window.ui.text_result.setText("")
              
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    # Create and show MainWindow
    mainWindow = MainWindow(img_source=0)
    mainWindow.show()
    
    # Start authenticator thread
    authenticator_thread = AuthenticatorThread(mainWindow)
    authenticator_thread.finished.connect(app.exit)
    authenticator_thread.start()

    sys.exit(app.exec_())
    
