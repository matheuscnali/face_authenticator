import face_recognition
import matplotlib as plt
import numpy as np

from PIL import Image, ImageDraw

class Authenticator:
    
    def __init__(self):
        
        self.known_face_encodings = np.array([])
        self.known_face_id = np.array([])

    def add_user(self, image, id):
        
        if face_recognition.face_encodings(image) == []:
            return False

        if len(self.known_face_encodings) == 0:
            self.known_face_encodings = np.hstack((self.known_face_encodings, face_recognition.face_encodings(image)[0]))
            self.known_face_id = np.hstack((self.known_face_id, id))
    
        else:
            self.known_face_encodings = np.vstack((self.known_face_encodings, face_recognition.face_encodings(image)[0]))
            self.known_face_id = np.hstack((self.known_face_id, id))
    
        return True
    
    def remove_user(self, id):
        
        self.known_face_encodings.remove(self.known_face_encodings.index(id))
        self.known_face_id.remove(self.known_face_id.index(id))

    def face_crop(self, image):

        def face_area(face):
            top, right, bottom, left = face
            return (bottom-top)*(right-left)
        
        faces_locations = face_recognition.face_locations(image)
        
        # Get the biggest bounding box.
        if faces_locations != []:
            curr_face = faces_locations[0]
            for face in faces_locations:
                if face_area(face) > face_area(curr_face):
                    curr_face = face
        
            return curr_face
        
        return faces_locations

    def face_classifier(self, image):

        face_location = face_recognition.face_locations(image)
        face_encoding = face_recognition.face_encodings(image, face_location)

        if face_encoding == []:
            return ("Face encoding is []", False)
        
        matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
       
        if True in matches:
            first_match_index = matches.index(True)
            name = self.known_face_id[first_match_index]

            return ("User '%s' detected." % (name), True)
        
        return ("User does not exist in database.", False)
        

            

        
