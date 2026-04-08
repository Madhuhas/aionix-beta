import speech_recognition as sr
import pyttsx3

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 180)

    def speak(self, text: str):
        self.tts.say(text)
        self.tts.runAndWait()

    def listen_once(self, prompt: str = "Listening..."):
        print(prompt)
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"[voice] {text}")
            return text
        except sr.UnknownValueError:
            print("I couldn't understand that.")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None
