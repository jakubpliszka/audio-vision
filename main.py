from enum import Enum
import time

from src.face_recognition import FaceRecognition
from src.camera import Camera
from src.speech import Speech

START_PHASE = "Pizza"

class State(Enum):
    STANDBY = 0
    CAMERA_RUN = 1
    LISTEN = 2
    TRAIN = 3

def main():
    speech = Speech()
    camera = Camera()
    face_recognition = FaceRecognition()
    
    speech.say("System initialized")
    state = State.STANDBY
    while True:
        match state:
            case State.STANDBY:
                speech.listen_for(START_PHASE)
                state = State.CAMERA_RUN
            case State.CAMERA_RUN:
                frame = camera.capture()
                if face_recognition.detect_face(frame).size == 0:
                    continue

                # check if person is recognized
                person = face_recognition.recognize(frame)
                if person:
                    speech.say(f"Hello {person}")
                    state = State.LISTEN
                else: # if not, add new person
                    state = State.TRAIN
            case State.LISTEN:
                heard = speech.listen()
                speech.say(f"You said {heard}")
            case State.TRAIN:
                speech.say("Please tell me your name")
                name = speech.listen() # get name from speech recognition
                id = face_recognition.add_new_person(name) # add new person to database
                speech.say("Please stand still and look at the camera")

                dataset = face_recognition.create_dataset(camera, 100) # create dataset
                face_recognition.train(dataset, id) # train the model
                speech.say("New person added to the database")
                state = State.CAMERA_RUN
        time.sleep(0.5)


        # dataset = face_recognition.create_dataset(camera, 100)
        # id = face_recognition.add_new_person("jakub")
        # face_recognition.train(dataset, id)

    



if __name__ == "__main__":
    main()
