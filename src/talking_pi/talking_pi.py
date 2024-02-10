import speech_recognition as sr
from gtts import gTTS
import datetime as dt
from subprocess import call
import os
from openai import OpenAI
from pydub import AudioSegment

class TalkingPi:

    def __init__(self):
        self._openai_client = OpenAI()
        self._tmp_path = "/app/talking_pi/tmp"

    @staticmethod
    def _play_wav(path: str):
        call(["aplay", path])

    def play_mp3(self, path: str):
        sound = AudioSegment.from_mp3(path)
        export_file_name = self._tmp_path + "wav_sound.wav"
        sound.export(export_file_name, format="wav")
        self._play_wav(export_file_name)
        os.remove(export_file_name)

    @staticmethod
    def quack():
        TalkingPi._play_wav("/app/src/resources/duck_quack.wav")

    def play_text_as_speech(self, text: str):
        tts = gTTS(text=text, lang='en')
        file_name = self._tmp_path + "response"+dt.datetime.now().strftime("%H-%M-%S")+".mp3"
        tts.save(file_name)
        self.play_mp3(file_name)
        os.remove(file_name)

    def get_gpt_response(self, question: str):
        messages_to_send = [
            {"role": "user", "content": "Please respond to the following question in 3-5 sentences: " + question}]
        completion = self._openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_to_send,
            max_tokens=300)
        return completion.choices[0].message.content



