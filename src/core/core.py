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

class Core:
    def __init__(self) -> None:
        self.speech = Speech()
        self.camera = Camera()
        self.face_recognition = FaceRecognition()

        self.speech.say("System initialized")
        self.state = State.STANDBY

    def get_name_from_speech(self) -> str:
        self.speech.say("Please tell me your name")
        name = None
        while not name:
            try:
                name = self.speech.listen() # get name from speech recognition
            except Exception:
                self.speech.say("Sorry, I could not understand you")
        return name

    def add_new_person(self) -> None:
        name = self.get_name_from_speech()

        id = self.face_recognition.add_new_person(name) # add new person to database
        self.speech.say("Please stand still and look at the camera")

        dataset = self.face_recognition.create_dataset(self.camera, 100) # create dataset
        self.face_recognition.train(dataset, id) # train the model
        self.speech.say("New person added to the database")

    def run(self) -> None:
        while True:
            match state:
                case State.STANDBY:
                    self.speech.listen_for(START_PHASE)
                    state = State.CAMERA_RUN
                case State.CAMERA_RUN:
                    frame = self.camera.capture()
                    if self.face_recognition.detect_face(frame).size == 0:
                        continue

                    # check if person is recognized
                    person = self.face_recognition.recognize(frame)
                    if person:
                        self.speech.say(f"Hello {person}")
                        state = State.LISTEN
                    else: # if not, add new person
                        state = State.TRAIN
                case State.LISTEN:
                    heard = self.speech.listen()
                    self.speech.say(f"You said {heard}")
                case State.TRAIN:
                    self.add_new_person()
                    state = State.CAMERA_RUN
            time.sleep(0.5)
