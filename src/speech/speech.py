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

    def listen(self) -> str:
        text = None
        # capture audio from microphone
        with self.microphone as source:
            audio = self.speech_recognizer.listen(source)
            try:
                # convert speech to text
                text = self.speech_recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                raise Exception("Sorry, I could not understand what you said")
            except sr.RequestError:
                raise Exception("Sorry, I could not access the Google Speech Recognition service")

    def listen_for(self, phrase: str) -> None:
        phrase = phrase.lower()
        text = None
        while True:
            text = self.listen()
            if text and phrase in text.lower():
                break # exit the loop if the phrase is recognized

    def say(self, text: str, log: bool = True) -> None:
        if log:
            print("Saying:", text)
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
