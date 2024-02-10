import speech_recognition as sr
from gtts import gTTS
import datetime as dt
from subprocess import call


class TalkingPi:
    @staticmethod
    def _playsound(*, wav_path: str):
        call(["aplay", wav_path])

    @staticmethod
    def quack():
        TalkingPi._playsound(wav_path="/app/src/resources/duck_quack.wav")

    def play_text_as_speech(self, text):
        tts = gTTS(text=text, lang='en')
        fname = "response"+dt.datetime.now().strftime("%H-%M-%S")+".mp3"
        tts.save(fname)
        self._playsound(wav_path=fname)

