import os
from .text_to_speech import TextToSpeech
from .audio_player import AudioPlayer
from .gpt_manager import GPTManager
from src.mood_prompts import Mood, main_header
import threading
import queue


class TalkingPi:

    def __init__(self, text_to_speech: TextToSpeech,
                 audio_player: AudioPlayer,
                 gpt_manager: GPTManager,
                 mood: Mood):
        self._text_to_speech = text_to_speech
        self._gpt_manager = gpt_manager
        self._audio_player = audio_player
        self._tmp_path = "/app/tmp/"
        self.mood = mood

        # Turn on audio worker to play items in queue
        threading.Thread(target=self._audio_player.work_on_audio_queue, daemon=True).start()

    def play_response_to_question(self, question: str):
        response = self.get_gpt_question_response(question)
        self.play_text_as_speech(response)

    def stream_response_to_question(self, question: str):
        for sentence in self._gpt_manager.stream_sentence_response_gen(question):
            print(f"Extracted sentence from GPT response: {sentence}")
            mp3_filepath = self._text_to_speech.create_mp3_from_text(sentence)
            self._audio_player.queue.put(mp3_filepath)
        print("Done handling sentences")
        self._audio_player.queue.join()
        print("Done")

    def quack(self):
        self._audio_player.play_wav("/app/src/resources/duck_quack.wav")

    def play_text_as_speech(self, text: str):
        mp3_filepath = self._text_to_speech.create_mp3_from_text(text)
        self._audio_player.play_mp3(mp3_filepath)
        os.remove(mp3_filepath)

    def get_gpt_question_response(self, question: str):
        return self._gpt_manager.get_gpt_response(main_header[self.mood] + question)