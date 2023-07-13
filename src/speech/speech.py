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

    def listen(self, timeout: int = 5, phrase_time_limit: int = 5) -> str:
        text = None
        # capture audio from microphone
        with self.microphone as source:
            try:
                audio = self.speech_recognizer.listen(source, timeout, phrase_time_limit)
                # convert speech to text
                
                text = self.speech_recognizer.recognize_google(audio)
                return text
            except sr.WaitTimeoutError:
                raise sr.WaitTimeoutError("Sorry, I could not hear you")
            except sr.UnknownValueError:
                raise sr.UnknownValueError("Sorry, I could not understand what you said")
            except sr.RequestError:
                raise sr.RequestError("Sorry, I could not access the Google Speech Recognition service")
        

    def listen_for(self, phrase: str | list[str], listen_once: bool = False) -> None:
        if type(phrase) is str:
            phrase = phrase.lower()
            is_str = True
        else:
            phrase = [p.lower() for p in phrase]
            is_str = False
            
        while True:
            try:
                text = self.listen(timeout=2, phrase_time_limit=2)
                if not text:
                    continue

                text = text.lower()
                if is_str and phrase in text:
                    break # exit the loop if the phrase is recognized
                elif not is_str and any(p in text for p in phrase):
                    break # exit the loop if the phrase is recognized
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                if listen_once:
                    raise

                continue

    def say(self, text: str, log: bool = True) -> None:
        if log:
            print("Saying:", text)
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
