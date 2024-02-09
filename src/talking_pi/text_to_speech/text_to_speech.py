#
# from pathlib import Path
#
# class SpeechRecogniser:
#     def __init__(self, directory: Path):
#         self._directory = directory
#         self._recognizer = sr.Recognizer()
#     def __call__(self, filename: str):
#         with sr.AudioFile(filename) as source:
#             audio = self._recognizer.record(source)
#         try:
#             text = self._recognizer.recognize_google_cloud(audio)
#             return text
#         except
