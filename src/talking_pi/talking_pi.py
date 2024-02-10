import speech_recognition as sr
from subprocess import call
import os
from openai import OpenAI
from pydub import AudioSegment
from .text_to_speech import TextToSpeech


class TalkingPi:

    def __init__(self, text_to_speech: TextToSpeech):
        self._openai_client = OpenAI()
        self._text_to_speech = text_to_speech
        self._tmp_path = "/app/tmp/"

    @staticmethod
    def _play_wav(path: str):
        call(["aplay", path])

    @staticmethod
    def quack():
        TalkingPi._play_wav("/app/src/resources/duck_quack.wav")

    def play_mp3(self, filepath: str):
        sound = AudioSegment.from_mp3(filepath)
        export_path = self._tmp_path + "wav_sound.wav"
        sound.export(export_path, format="wav")
        self._play_wav(export_path)
        os.remove(export_path)

    def play_text_as_speech(self, text: str):
        mp3_filepath = self._text_to_speech.create_mp3_from_text(text)
        self.play_mp3(mp3_filepath)
        os.remove(mp3_filepath)

    def get_gpt_response(self, question: str):
        messages_to_send = [
            {"role": "user", "content": "Please respond to the following question in 3-5 sentences: " + question}]
        completion = self._openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_to_send,
            max_tokens=300)
        return completion.choices[0].message.content



