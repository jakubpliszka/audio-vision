import cv2
import os
import numpy as np

from src.camera import Camera

# TODO add a database to store the faces and their labels


class FaceRecognition:
    FACE_IMAGE_SIZE = (256, 256)
    CONFIDENCE_THRESHOLD = 100

    def __init__(self, cascade_path: str = "haarcascade_frontalface_default.xml") -> None:
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        # initialize the camera
        self.camera = Camera()

    def train(self, faces: list[np.ndarray], ids: list[int]) -> None:
        self.recognizer.train(faces, ids)
        # save the model
        # self.recognizer.write("face_recognition_model.yml")

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

            # replace the face with the processed face
            result[i] = face

        return result

    def recognize(self, image: np.ndarray) -> bool:
        # detect the faces in the frame using the face detection classifier
        detected_faces = self.detect_face(image)

        result = []
        # loop over each detected face
        for face in detected_faces:
            # use the face recognition model to recognize the person
            id, confidence = self.recognizer.predict(face)

            person = {
                "recognized": False,
                "id": None,
            }

            # if the confidence is high enough, the person is recognized
            if confidence > self.CONFIDENCE_THRESHOLD:
                person["recognized"] = True
                person["id"] = id

            result.append(person)

        return result

    def create_dataset(self, name: str, number_of_images: int = 1) -> None:
        # create a directory to store the images
        directory = os.path.join("dataset", name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # start the loop to capture images
        for i in range(number_of_images):
            # read a frame from the camera
            frame = self.camera.capture()
            detected_faces = self.detect_face(frame)

            for face in detected_faces:
                img_path = f"{directory}/{name}_{i}.jpg"
                cv2.imwrite(img_path, face)
