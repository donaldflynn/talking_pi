import speech_recognition as sr
from gtts import gTTS
import pygame
import time
import datetime as dt
import playsound


class TalkingPi:

    def __init__(self):
        pass

    # def transcribe_audio(self):
    #     # f = sr.AudioFile(self.filename)
    #     recognizer = sr.Recognizer()
    #     # Load the audio file
    #     with sr.AudioFile(self.filename) as source:
    #         audio = recognizer.record(source)
    #
    #     try:
    #         # Transcribe the audio using Google Web Speech API
    #         text = recognizer.recognize_google_cloud(audio)
    #         return text
    #     except sr.UnknownValueError:
    #         return "Google Speech Recognition could not understand the audio"
    #     except sr.RequestError as e:
    #         return f"Could not request results from Google Speech Recognition service; {e}"

    def play_text_as_speech(self, text):
        tts = gTTS(text=text, lang='en')
        fname = "response"+dt.datetime.now().strftime("%H-%M-%S")+".mp3"
        tts.save(fname)
        playsound(fname)

    @staticmethod
    def quack():
        playsound("/code/src/resources/duck_quack.wav")
