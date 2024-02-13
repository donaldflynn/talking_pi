import pyaudio
import wave
from pydub import AudioSegment
import os
import datetime as dt
import queue
import threading


class AudioPlayer:
    #    +----------------------+          +---------------------+
    #    |      mp3_queue       |    -->   |    mp3_converter    |
    #    |                      |          |       worker        |
    #    +----------------------+          +---------------------+
    #                                                 |
    #                                                 v
    #
    #     +---------------------+           +---------------------+
    #     |       wav_player    |   <--     |      wav_queue      |
    #     |          worker     |           |                     |
    #     +---------------------+           +---------------------+

    def __init__(self):
        self._chunk = 1024 # How many bytes to process at once when playing a wav file
        self._tmp_path = "/app/tmp/"
        self._audio_card = os.environ["AUDIO_CARD"]
        self._mp3_queue = queue.Queue()
        self._wav_queue = queue.Queue()
        self._handling_mp3_item = threading.Event()
        self.finished_handling_audio = threading.Event()
        self.finished_adding_to_queues = threading.Event()

        # Turn on workers to handle items in queue
        threading.Thread(target=self._mp3_converter_worker, daemon=True).start()
        threading.Thread(target=self._wav_player_worker, daemon=True).start()

    def put_item_in_mp3_playing_queue(self, filepath: str):
        self._mp3_queue.put(filepath)

    def play_wav(self, filepath: str):
        with wave.open(filepath, 'rb') as wf:
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

    def _play_and_remove_wav(self, filepath: str):
        self.play_wav(filepath)
        os.remove(filepath)

    def play_mp3(self, filepath: str):
        wav_filepath = self._prepare_mp3_to_wav(filepath)
        self.play_wav(wav_filepath)
        os.remove(wav_filepath)

    def _prepare_mp3_to_wav(self, filepath: str) -> str:
        sound = AudioSegment.from_mp3(filepath)
        export_path = self._tmp_path + f"{dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')}.wav"
        sound.export(export_path, format="wav")
        return export_path

    def _is_mp3_worker_active(self):
        return self._mp3_queue.qsize() != 0 or self._handling_mp3_item.is_set()

    def _mp3_converter_worker(self):
        while True:
            mp3_path = self._mp3_queue.get()
            self.finished_handling_audio.clear()
            self._handling_mp3_item.set()
            print(f"Handling mp3 file in queue: {mp3_path}")
            wav_path = self._prepare_mp3_to_wav(mp3_path)
            self._wav_queue.put(wav_path)
            os.remove(mp3_path)
            self._handling_mp3_item.clear()
            print(f"Finished handling mp3 file. Remaining items in queue: {self._mp3_queue.qsize()}")

    def _wav_player_worker(self):
        while True:
            wav_path = self._wav_queue.get()
            print(f"Handling wav file in queue: {wav_path}")
            self._play_and_remove_wav(wav_path)
            print(f"Finished handling mp3 file. Remaining items in queue: {self._wav_queue.qsize()}")

            if (self._wav_queue.qsize() == 0
                    and not self._is_mp3_worker_active()
                    and self.finished_adding_to_queues.is_set()):
                print("Finished handling audio queues")
                self.finished_handling_audio.set()


