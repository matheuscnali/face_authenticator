import sys
import cv2
import random
import time
import matplotlib.pyplot as plt
import traceback
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

        self.authenticator = Authenticator()

        self.ui.add_user.clicked.connect(self.add_user)
        self.ui.remove_user.clicked.connect(self.remove_user)
        
        # Create video capture.
        self.cap = cv2.VideoCapture(source)
        self.image = self.cap.read()[1]

        self.threadpool = QtCore.QThreadPool()

        """ Image timer thread. """
        # Create a timer.
        self.timer_images = QtCore.QTimer(self)
        self.control_timer_images(delay=20)     

        # Set timer timeout callback function.
        self.timer_images.timeout.connect(self.update_cam_image)

        # Pass the function to execute
        worker = Worker(self.run_authenticator) # Any other args, kwargs are passed to the run function
        
        # Execute
        self.threadpool.start(worker) 
    
    def add_user(self):

        while True:

            image = cv2.imread("example.jpeg")
            face_location = self.authenticator.face_crop(image)

            if face_location != []:
                top, right, bottom, left = face_location

                if self.authenticator.add_user(image[top:bottom, left:right], self.ui.id_text.toPlainText()):
                    break
            
            time.sleep(0.1)

    def remove_user(self):

        self.authenticator.remove_user(self.ui.id_text.toPlainText())
    
    def run_authenticator(self):
        
        while True:
            
            image = cv2.imread("example.jpeg")
            face_location = self.authenticator.face_crop(image)
    
            if face_location != []:
                top, right, bottom, left = face_location
                face = image[top:bottom, left:right]
                classification_result = self.authenticator.face_classifier(face)
            
                if classification_result[1]:
                    life_proof_result = self.authenticator.life_proof(face)
                    if life_proof_result:
                        self.ui.image_result.setVisible(True)
                        self.ui.text_result.setText("%s\nPassed in life proof." %(classification_result[0]))
                        self.ui.image_result.setPixmap(QtGui.QPixmap("data/gui_images/check.png"))
                    
                    else:
                        self.ui.image_result.setVisible(True)
                        self.ui.text_result.setText("%s\nFailed in life proof." %(classification_result[0]))
                        self.ui.image_result.setPixmap(QtGui.QPixmap("data/gui_images/alert.png"))

                elif classification_result[0] == "User does not exist in database.":
                    self.ui.image_result.setVisible(True)
                    self.ui.text_result.setText(classification_result[0])
                    self.ui.image_result.setPixmap(QtGui.QPixmap("data/gui_images/alert.png"))

            time.sleep(2)            
            self.ui.text_result.setText("")
            self.ui.image_result.setVisible(False)

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

class Worker(QtCore.QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
    
    @QtCore.pyqtSlot()
    def run(self):

        self.fn()
                     
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    # Create and show MainWindow.
    mainWindow = MainWindow(source=0)
    mainWindow.show()

    sys.exit(app.exec_())