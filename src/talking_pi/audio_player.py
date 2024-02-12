import pyaudio
import wave
from pydub import AudioSegment
import os
import datetime as dt


class AudioPlayer:
    def __init__(self):
        self._chunk = 1024
        self._tmp_path = "/app/tmp/"
        self._audio_card = os.environ["AUDIO_CARD"]

    def play_wav(self, path: str):
        with wave.open(path, 'rb') as wf:
            p = pyaudio.PyAudio()
            # Open stream (2)
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            # Play samples from the wave file (3)
            while len(data := wf.readframes(self._chunk)):  # Requires Python 3.8+ for :=
                stream.write(data)

            # Close stream (4)
            stream.close()

            # Release PortAudio system resources (5)
            p.terminate()

    def play_mp3(self, filepath: str):
        sound = AudioSegment.from_mp3(filepath)
        export_path = self._tmp_path + "wav_sound.wav"
        sound.export(export_path, format="wav")
        self.play_wav(export_path)
        os.remove(export_path)

    def play_mp3_in_queue_gen(self, filepath: str):
        sound = AudioSegment.from_mp3(filepath)
        export_path = self._tmp_path + f"{dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')}.wav"

