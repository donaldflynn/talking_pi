import pyaudio
import wave
from pydub import AudioSegment
import datetime as dt
import queue
import threading
import os
import time


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

    def _play_wav(self, filepath: str, audio_interface):
        with wave.open(filepath, 'rb') as wf:
            with AudioStreamOpener(audio_interface, wf) as stream:
                while len(data := wf.readframes(self._chunk)):  # Requires Python 3.8+ for :=
                    stream.write(data)

    def play_wav(self, filepath: str):
        self._wav_queue.put(WavQueueItem(filepath, remove=False))

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
            with QueueHandlerLogger(mp3_path, self._mp3_queue):
                wav_path = self._prepare_mp3_to_wav(mp3_path)
                self._wav_queue.put(wav_path)
                os.remove(mp3_path)
                self._handling_mp3_item.clear()

    def _wav_player_worker(self):
        with PyaudioInitialiser as audio_interface:
            while True:
                wav_queue_item = self._wav_queue.get()
                with QueueHandlerLogger(wav_queue_item.filepath, self._wav_queue):
                    self._play_wav(wav_queue_item.filepath, audio_interface)
                    if wav_queue_item.remove:
                        os.remove(wav_queue_item.filepath)

                if (self._wav_queue.qsize() == 0
                        and not self._is_mp3_worker_active()
                        and self.finished_adding_to_queues.is_set()):
                    print("Finished handling audio queues")
                    self.finished_handling_audio.set()


class QueueHandlerLogger:
    def __init__(self, filepath, queue):
        self.filepath = filepath
        self.start_time = None
        self._queue = queue

    def __enter__(self):
        self.start_time = time.time()
        print(f"Handling file in queue: {self.filepath}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:  # If code completed without error
            print(f"Finished handling item {self.filepath} in {time.time() - self.start_time} seconds. Remaining items in queue: {self._queue.qsize()}")


class AudioStreamOpener:
    def __init__(self, audio_interface: pyaudio.PyAudio, file: wave.Wave_read):
        self._audio_interface = audio_interface
        self._wf = file
        self._stream = None

    def __enter__(self):
        stream = self._audio_interface.open(format=self._audio_interface.get_format_from_width(self._wf.getsampwidth()),
                                            channels=self._wf.getnchannels(),
                                            rate=self._wf.getframerate(),
                                            output=True)
        return stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stream.close()
        self._audio_interface = None


class PyaudioInitialiser:
    def __init__(self):
        self._audio_interface = None

    def __enter__(self):
        self.audio_interface = pyaudio.PyAudio()
        return self.audio_interface

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.audio_interface.terminate()
        self._audio_interface = None


class WavQueueItem:
    def __init__(self, filepath, remove=False):
        self.filepath = filepath
        self.remove = remove
