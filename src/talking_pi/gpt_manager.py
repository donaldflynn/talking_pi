import time
from openai import OpenAI


class GPTManager:
    def __init__(self):
        self._openai_client = OpenAI()
        self._max_tokens_per_request = 300
        self._model = "gpt-3.5-turbo"

    def _get_gpt_response(self, text: str):
        messages_to_send = [
            {"role": "user", "content": text}]
        completion = self._openai_client.chat.completions.create(
            model=self._model,
            messages=messages_to_send,
            max_tokens=self._max_tokens_per_request)
        return completion.choices[0].message.content
    def get_gpt_response(self, text: str):
        start_time = time.time()
        print(f"Sending message to gpt: {text}")
        response = self._get_gpt_response(text)
        print(f"Recieved response in {time.time() - start_time} seconds from gpt: {response}")
        return response

    def stream_sentence_response_gen(self, text: str):
        messages_to_send = [
            {"role": "user", "content": text}]
        completion_gen = self._openai_client.chat.completions.create(
            model=self._model,
            messages=messages_to_send,
            max_tokens=self._max_tokens_per_request,
            stream=True)
        current_response = ""
        try:
            while True:
                is_sentence = False
                while not is_sentence:
                    current_response += next(completion_gen)
                    if current_response.endswith(("!", ".", "?")):
                        yield current_response
                        is_sentence = True
                        current_response = ""
        except StopIteration:
            if current_response != "":
                yield current_response
