import os
from openai import OpenAI
from .text_to_speech import TextToSpeech
from .audio_player import AudioPlayer
from src.mood_prompts import Mood, main_header
import time


class TalkingPi:

    def __init__(self, text_to_speech: TextToSpeech,
                 audio_player: AudioPlayer,
                 mood: Mood):
        self._openai_client = OpenAI()
        self._text_to_speech = text_to_speech
        self._audio_player = audio_player
        self._tmp_path = "/app/tmp/"
        self.mood = mood

    def play_response_to_question(self, question: str):
        response = self.get_gpt_question_response(question)
        self.play_text_as_speech(response)

    def quack(self):
        self._audio_player.play_wav("/app/src/resources/duck_quack.wav")

    def play_text_as_speech(self, text: str):
        mp3_filepath = self._text_to_speech.create_mp3_from_text(text)
        self._audio_player.play_mp3(mp3_filepath)
        os.remove(mp3_filepath)

    def get_gpt_question_response(self, question: str):
        return self._get_gpt_response(main_header[self.mood] + question)

    def _get_gpt_response(self, text: str):
        start_time = time.time()
        messages_to_send = [
            {"role": "user", "content": text}]
        print(f"Sending messages to gpt: {messages_to_send}")
        completion = self._openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_to_send,
            max_tokens=300)
        response = completion.choices[0].message.content
        print(f"Recieved response in {time.time() - start_time} seconds from gpt: {response}")
        return response

