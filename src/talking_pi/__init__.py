from .talking_pi import TalkingPi, Mood
from .text_to_speech import TextToSpeech
from .audio_player import AudioPlayer
from .gpt_manager import GPTManager


def create_talking_pi():
    player = AudioPlayer()
    speech = TextToSpeech()
    gpt = GPTManager()
    return TalkingPi(speech, player, gpt, Mood.ANGRY)
