from enum import Enum

from src.face_recognition import FaceRecognition
from src.camera import Camera
from src.speech import Speech
from src.llm import LLM
from src.aspen_api import AspenAPI


class State(Enum):
    STANDBY = 0
    CAMERA_RUN = 1
    LISTEN = 2
    TRAIN = 3

class Core:
    DATASET_SIZE = 100
    FACE_DETECTION_LIMIT = 100
    PERSON_RECOGNITION_LIMIT = 50

    START_PHASE = ["hey aspen", "hello aspen", "hi aspen", "aspen"]
    OPEN_TRAY_PHASE = "open the tray"
    CLOSE_TRAY_PHASE = "close the tray"


    def __init__(self, use_camera: bool = True, use_aspen: bool = True) -> None:
        self.use_camera = use_camera
        self.use_aspen = use_aspen

        self.speech = Speech()
        self.face_recognition = FaceRecognition()
        self.llm = LLM()

        if use_camera:
            self.camera = Camera()

        if use_aspen:
            self.aspen = AspenAPI()

        self.speech.say("System initialized")
        self.state = State.STANDBY

    def change_state(self, state: State) -> None:
        self.state = state
        self.speech.say(f"Changed state to {state.name}")

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
        while True:
            name = self.get_name_from_speech()
            self.speech.say(f"I heard {name}, is that correct?")
            try:
                self.speech.listen_for("yes", listen_once=True)
                break
            except Exception:
                continue

        id = self.face_recognition.add_new_person(name) # add new person to database
        self.speech.say("Please stand still and look at the camera")

        dataset = self.face_recognition.create_dataset(self.camera, self.DATASET_SIZE) # create dataset
        self.face_recognition.train(dataset, id) # train the model
        self.speech.say("New person added to the database")

    def run(self) -> None:
        while True:
            match self.state:
                case State.STANDBY:
                    self.speech.listen_for(self.START_PHASE)
                    self.change_state(State.CAMERA_RUN)
                case State.CAMERA_RUN:
                    if not self.use_camera:
                        self.change_state(State.LISTEN)
                        continue

                    person = self.recognize()

                    if person:
                        self.change_state(State.LISTEN)
                    else: # if not, add new person
                        self.speech.say("I don't know who you are, starting training...")
                        self.change_state(State.TRAIN)
                case State.LISTEN:
                    try:
                        self.speech.say("I'm listening")
                        heard = self.speech.listen()
                        heard = heard.lower()

                        if self.use_aspen:
                            if heard == self.OPEN_TRAY_PHASE:
                                self.aspen.open_tray()
                                continue
                            elif heard == self.CLOSE_TRAY_PHASE:
                                self.aspen.open_tray()
                                continue

                        response_message = self.llm.chat(heard)
                        self.speech.say(response_message)
                    except Exception as exception:
                        self.speech.say(str(exception))
                    finally:
                        self.change_state(State.STANDBY)
                case State.TRAIN:
                    self.add_new_person()
                    self.change_state(State.CAMERA_RUN)

    def recognize(self) -> str:
        face_detected_counter = 0
        recognized_persons = {}

        while face_detected_counter < self.FACE_DETECTION_LIMIT:
            frame = self.camera.capture()
            if self.face_recognition.detect_face(frame).size == 0:
                continue
            
            face_detected_counter += 1
            
            # check if person is recognized
            person = self.face_recognition.recognize(frame)
            if person:
                recognized_persons[person] = recognized_persons.get(person, 0) + 1 # count how many times a person is recognized
                if recognized_persons[person] >= self.PERSON_RECOGNITION_LIMIT:
                    self.speech.say(f"Hello {person}")
                    return person
                
        return None