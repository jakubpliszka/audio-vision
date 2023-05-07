import speech_recognition as sr
import pyttsx3 as tts


class Speech:
    def __init__(self) -> None:
        # create a speech recognition object
        self.speech_recognizer = sr.Recognizer()

        # create a microphone object
        self.microphone = sr.Microphone()

        # create a text-to-speech object
        self.tts_engine = tts.init()

        # use the system's default voice
        voices = self.tts_engine.getProperty("voices")
        self.tts_engine.setProperty("voice", voices[0].id)

        self.say("Hello")

    def listen(self) -> str:
        text = None
        # capture audio from microphone
        with self.microphone as source:
            self.say("Speak Anything")
            audio = self.speech_recognizer.listen(source)
            try:
                # convert speech to text
                text = self.speech_recognizer.recognize_google(audio)

                # speak the text
                self.say(text)
            except sr.UnknownValueError:
                self.say("Sorry, I could not understand what you said")
            except sr.RequestError:
                self.say(
                    "Sorry, I could not access the Google Speech Recognition service")
            finally:
                return text

    def say(self, text: str, log: bool = True) -> None:
        if log:
            print("Saying:", text)
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
