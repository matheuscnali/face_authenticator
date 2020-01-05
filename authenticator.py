import argparse
import imutils
import cv2
import face_recognition
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from imutils import contours
from skimage import measure, img_as_ubyte
from PIL import Image, ImageDraw

class Authenticator:
    
    def __init__(self):
        
        self.known_face_encodings = np.empty((0, 128))
        self.known_face_id = np.empty(0)

    def add_user(self, image, user_id):

        self.known_face_encodings = np.append(self.known_face_encodings, [face_recognition.face_encodings(image)[0]], axis=0)
        self.known_face_id = np.append(self.known_face_id, [user_id], axis=0)
    
    def remove_user(self, user_id):

        ids = np.where(self.known_face_id == user_id)

        self.known_face_id = np.delete(self.known_face_id, ids)
        self.known_face_encodings = np.delete(self.known_face_encodings, ids, 0)

    def face_crop(self, image):

        def get_bb_area(face):
            top, right, bottom, left = face
            return (bottom-top)*(right-left)
        
        # Getting faces bounding boxes
        faces_bb = face_recognition.face_locations(image)
        
        # Get the biggest bounding box
        if faces_bb:
            return max(faces_bb, key=get_bb_area)
        else:
            return False

    def face_classifier(self, face_img):

        face_encoding = face_recognition.face_encodings(face_img)

        if not face_encoding:
            return False
        
        # Check for similar face with tolerance of 0.6
        matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
       
        if True in matches:
            first_match_index = matches.index(True)
            name = self.known_face_id[first_match_index]
            return "User '%s' detected." % (name)
        else:
            return False

    def life_proof(self, face_img, debug=False):
        
        def save_img(img, name, ):
            cv2.imwrite(str('results/%s/%s.png' %(curr_time, name)), img)

        def width_reescale(image, width):

            scale = width / image.shape[1]
            new_dim = (width, int(image.shape[0] * scale))
            return cv2.resize(image, new_dim, interpolation = cv2.INTER_AREA)

        # Reescale to 800px width
        face_img_reescaled = width_reescale(face_img, width=800)

        # Convert to gray scale
        gray = cv2.cvtColor(face_img_reescaled, cv2.COLOR_BGR2GRAY)

        # Contrast equalization
        clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
        grayEq = clahe.apply(gray)

        # Reescale ROI 500px width
        grayEq_reescaled = width_reescale(grayEq, width=500) 

        # Apply Blur to remove high frequency noise
        blurred = cv2.GaussianBlur(grayEq_reescaled, (3, 3), 0)

        # Apply threshold to highlight dots
        thresh = cv2.threshold(blurred, 170, 255, cv2.THRESH_BINARY)[1]

        # Connected components analysis to generate a blobs mask
        labels = measure.label(thresh, connectivity=2, background=0)
        mask = np.zeros(thresh.shape, dtype="uint8")

        # Removing outliers (too big or small blobs)
        minBlob = 100; maxBlob = 5000
        for label in np.unique(labels):
            # if this is the background label, ignore it
            if label == 0:
                continue

            # otherwise, construct the label mask and count the
            # number of pixels
            labelMask = np.zeros(thresh.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)

            # Adding blobs that are inside the limits
            if minBlob < numPixels < maxBlob:
                mask = cv2.add(mask, labelMask)

        # Find image contours
        cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        pts = [] # List of selected dots
        for c in cnts:
            ((cX, cY), radius) = cv2.minEnclosingCircle(c)
            if 5 < radius < 30: # Filter blobs by radius size
                if 120 < cX < grayEq.shape[1] - 120: # Removing 120px of each side to focus in the center of the face
                    if 100 < cY < grayEq.shape[0] - 100:
                        cv2.circle(grayEq, (int(cX), int(cY)), int(radius),
                                  (0, 0, 255), 2)
                        pts.append((cX, cY))

        if(len(pts) < 10):
            print('Failed in life proof, number of dots if too low. Number of Dots: %s' % str(len(pts)))
            return False
        else:
            print('Number of Dots: %s' % str(len(pts)))

        # Analysing each line (Dots are analysed by OpenCV from left to right, top to bottom)
        # Lines are determined by the variation of the Y values

        last_Y = 0
        lines_num = 0
        first_iteration = True
        line_change = False
        y_lines = [] # List with Y values of dots of a line, the variance of that line will determine how much it's bended
        temp_x_list = []; temp_y_list = [] # Temporary lines for plotting
        for (x, y) in pts:
            if not first_iteration:
                if line_change: # When the line changes, the temporary line list is saved in the main line list
                    y_lines.append(temp_y_list)
                    plt.plot(temp_x_list, temp_y_list) # Plotting the line dots
                    plt.scatter(temp_x_list[:], temp_y_list[:] ) # Plotting the points of that line
                    
                    # Reseting lists for the next line
                    temp_x_list = []; temp_y_list = []
                    temp_x_list.append(x)
                    temp_y_list.append(y)
                    line_change = False

                else:
                    if abs(last_Y - y) < 10:  # Check if the current point is in another line
                        temp_x_list.append(x) 
                        temp_y_list.append(y)
                    else:
                        lines_num += 1
                        line_change = True

            last_Y = y # Saving the last Y to check if there is a line change
            first_iteration  = False

        print('Number of lines: %s\n' % lines_num)

        if lines_num == 0:
            print ('Failed in file proof\n'); print('-----------------------------------------\n')
            return False

        # Computing the variance of each line and the variance between all the lines
        total_var = 0 # Cumulative variance, used to compute the average
        for i in range(lines_num-1):
            line_var = np.var(y_lines[i])
            print('Line Variance %s: %.2f\n' % ((i+1), int(line_var))) # Compute the variance of Y coordinate of the dots in a line
            if line_var > 0.0:
                total_var += line_var # Accumulate in this variable
            else:
                lines_num -= 1

        total_var = total_var / lines_num # Average

        print('Total variance average: %.2f' % int(total_var))

        colorEqCrop = cv2.cvtColor(grayEq, cv2.COLOR_GRAY2RGB) # Converting grayscale to colored 

        if debug:
            curr_time = time.ctime()
            os.mkdir('results/%s' % curr_time)
            
            save_img(face_img, '1_face_img')
            save_img(face_img, '2_face_img_reescaled')
            save_img(gray, '3_gray')
            save_img(grayEq, '4_grayEq')
            save_img(grayEq_reescaled, '5_grayEq_reescaled')
            save_img(blurred, '6_blurred')
            save_img(thresh, '7_thresh')
            save_img(colorEqCrop, '8_colorEqCrop')

        # Printing results
        if total_var > 5:
            print ('Sucess in life proof\n'); print('-----------------------------------------\n')
            return True
        else:
            print ('Failed in file proof\n'); print('-----------------------------------------\n')
            return False
        
