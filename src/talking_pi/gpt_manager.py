import time
from openai import OpenAI
from typing import Optional


class GPTManager:
    def __init__(self):
        self._openai_client = OpenAI()
        self._max_tokens_per_request = 300
        self._model = "gpt-3.5-turbo"

    def _get_gpt_response(self, text: str) -> str:
        messages_to_send = [
            {"role": "user", "content": text}]
        completion = self._openai_client.chat.completions.create(
            model=self._model,
            messages=messages_to_send,
            max_tokens=self._max_tokens_per_request)
        return completion.choices[0].message.content

    def get_gpt_response(self, text: str) -> str:
        start_time = time.time()
        print(f"Sending message to gpt: {text}")
        response = self._get_gpt_response(text)
        print(f"Recieved response in {time.time() - start_time} seconds from gpt: {response}")
        return response

    def stream_sentence_response_gen(self, text: str) -> Optional[str]:
        messages_to_send = [
            {"role": "user", "content": text}]
        completion_gen = self._openai_client.chat.completions.create(
            model=self._model,
            messages=messages_to_send,
            max_tokens=self._max_tokens_per_request,
            stream=True)
        current_response = ""
        for completion in completion_gen:
            next_item = completion.choices[0]
            if next_item.finish_reason is not None:
                print(next_item.finish_reason)
                break
            next_token = next_item.delta.content
            print(next_token)
            current_response += next_token
            if (current_response.endswith(("!", ".", "?", ":", ";")) or
                    (len(current_response) > 20 and current_response.endswith(","))):
                yield current_response
                current_response = ""
        if current_response != "":
            yield current_response

    def test_streaming(self):
        messages_to_send = [
            {"role": "user", "content": "Count to 20"}]
        completion_gen = self._openai_client.chat.completions.create(
            model=self._model,
            messages=messages_to_send,
            max_tokens=self._max_tokens_per_request,
            stream=True)
        try:
            while True:
                print(next(completion_gen).choices[0].delta.content)
        except StopIteration:
            print("Finished")
