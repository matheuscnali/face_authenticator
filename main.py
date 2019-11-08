import sys
import cv2
import functools
from PyQt5 import QtCore, QtGui, QtWidgets

from view import Ui_MainWindow
from authenticator import Authenticator


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """ Image timer thread. """
        # Create a timer.
        self.timer_images = QtCore.QTimer(self)
        self.controlTimer_images(source_1=0, source_2=2, delay=20)     

        # Set timer timeout callback function.
        self.timer_images.timeout.connect(self.viewCam)

    def viewCam(self):

        # Read image in BGR format.
        _, image_1 = self.cap_1.read()
        _, image_2 = self.cap_2.read()

        # Convert image to RGB format.
        image_1 = cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB)
        image_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB)

        # Get image infos.
        height_1, width_1, channel_1 = image_1.shape
        step_1 = channel_1 * width_1

        height_2, width_2, channel_2 = image_2.shape
        step_2 = channel_2 * width_2

        # Create QImage from image.
        qImg_1 = QtGui.QImage(image_1.data, width_1, height_1, step_1, QtGui.QImage.Format_RGB888)
        qImg_2 = QtGui.QImage(image_2.data, width_2, height_2, step_2, QtGui.QImage.Format_RGB888)
        
        # Show image in img_label.
        self.ui.img_cam_frontal.setPixmap(QtGui.QPixmap.fromImage(qImg_1))
        self.ui.img_cam_side.setPixmap(QtGui.QPixmap.fromImage(qImg_2))

    def controlTimer_images(self, source_1, source_2, delay):

        if not self.timer_images.isActive():
            # Create video capture.
            self.cap_1 = cv2.VideoCapture(source_1)
            self.cap_2 = cv2.VideoCapture(source_2) 
            
            # Start timer.
            self.timer_images.start(delay)

        else:
            # Stop timer.
            self.timer_images.stop()
            # Release video capture.
            self.cap_1.release()
            self.cap_2.release()
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # Create and show MainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())

