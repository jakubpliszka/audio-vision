import cv2
import datetime
import os
import numpy as np

from src.camera import Camera
from src.mongodb import MongoDB

# TODO find a way to save the recognizer to database 
# it should have IDs of all the people it has been trained on

class FaceRecognition:
    FACE_IMAGE_SIZE = (256, 256)
    CONFIDENCE_THRESHOLD = 50
    COLLECTION_NAME = "people"
    DB_NAME = "face_recognition"
    model_file = "face_recognition_model.yml"

    def __init__(self, cascade_path: str = "haarcascade_frontalface_default.xml", model_path: str = model_file) -> None:
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.trained = False

        if model_path and os.path.exists(model_path):
            self.recognizer.read(model_path)
            self.trained = True
            self.model_file = model_path

        self.database = MongoDB("localhost", 27017, self.DB_NAME)
        self.database.connect()

    def add_new_person(self, name: str) -> int:
        name = name.lower()

        # check if the person already exists
        person = self.database.find(self.COLLECTION_NAME, {"name": name})
        if person:
            return person["id"] 

        # get the id of the latest person
        latest_entry = self.database.find(self.COLLECTION_NAME, {}, sort=[("timestamp", -1)])
        if not latest_entry:
            # create a new entry
            id = 0
        else:
            id = latest_entry["id"] + 1 

        person = {
            "timestamp": datetime.datetime.now(),
            "name": name,
            "id": id,
        }

        # add a new person to the database
        self.database.insert(self.COLLECTION_NAME, person)

        # return the id of the new person
        return id

    def train(self, faces: list[np.ndarray], id: int) -> None:
        ids = np.full(len(faces), id, dtype=np.int32)
        if not self.trained:
            self.recognizer.train(faces, ids)
            self.trained = True
        else:
            self.recognizer.update(faces, ids)

        # save the model
        self.recognizer.write(self.model_file)

    def detect_face(self, image: np.ndarray) -> np.ndarray:
        detected_faces = self.face_cascade.detectMultiScale(
            image, scaleFactor=1.3, minNeighbors=5)

        result = np.empty((len(detected_faces), *self.FACE_IMAGE_SIZE))
        for i, face in enumerate(detected_faces):
            (x, y, w, h) = face
            # crop and resize the face region to a fixed size
            face = image[y:y+h, x:x+w]
            face = cv2.resize(face, self.FACE_IMAGE_SIZE)
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            # store the face in the result array
            result[i] = face

        return result

    def recognize(self, image: np.ndarray) -> str:
        if not self.trained:
            return None
        
        # detect the faces in the frame using the face detection classifier
        detected_faces = self.detect_face(image)
        face = detected_faces[0] # focus on the first face
        
        # use the face recognition model to recognize the person
        id, confidence = self.recognizer.predict(face)

        # if the confidence is high enough, the person is recognized
        if confidence < self.CONFIDENCE_THRESHOLD:
            return self.get_person_name(id)
        else:
            return None

    def create_dataset(self, camera: Camera, size: int) -> list:
        dataset = []
        cv2.namedWindow("Camera View", cv2.WINDOW_NORMAL)
        
        for _ in range(size):
            # read a frame from the camera
            frame = camera.capture()

            # detect the face in the frame
            detected_faces = self.detect_face(frame)
            if len(detected_faces) == 0:
                raise Exception("No face detected")
            elif len(detected_faces) > 1:
                raise Exception("Multiple faces detected")

            # save the face image
            face = detected_faces[0]
            dataset.append(face)
            
            # display the camera view
            cv2.imshow("Camera View", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyWindow("Camera View")
        return dataset
    
    def get_person_name(self, id: int) -> str:
        person = self.database.find(self.COLLECTION_NAME, {"id": id})
        return person["name"]
    