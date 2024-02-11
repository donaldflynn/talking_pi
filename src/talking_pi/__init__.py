from .talking_pi import TalkingPi, Mood
from .text_to_speech import TextToSpeech
from .audio_player import AudioPlayer


def create_talking_pi():
    player = AudioPlayer()
    speech = TextToSpeech()
    return TalkingPi(speech, player, Mood.ANGRY)
