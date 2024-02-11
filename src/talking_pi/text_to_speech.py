from google.cloud import texttospeech
import datetime as dt
import time


class TextToSpeech:

    def __init__(self):
        self._client = texttospeech.TextToSpeechClient()
        self._voice = texttospeech.VoiceSelectionParams(
            language_code="en-GB", name="en-GB-Wavenet-B"
        )
        self._audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        # Directory where file is saved
        self._tmp_path = "/app/tmp"

    def create_mp3_from_text(self, text: str) -> str:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        start_time = time.time()
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        print(f"Sending to text-to-speech API: {text} ")
        response = self._client.synthesize_speech(
            input=synthesis_input, voice=self._voice, audio_config=self._audio_config
        )
        file_path = self._tmp_path + "response" + dt.datetime.now().strftime("%H-%M-%S") + ".mp3"
        print(f"Recieved response in {time.time() - start_time} seconds")
        # The response's audio_content is binary.
        with open(file_path, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f'Audio content written to file "{file_path}"')
        return file_path
