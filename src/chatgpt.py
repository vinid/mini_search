import openai
from tqdm.contrib.concurrent import thread_map


class ChatGPTWrapper:
    def __init__(self, api_key, model_name="gpt-3.5-turbo"):
        """
        Currently only handles single message sessions.
        """
        self.model_name = model_name
        openai.api_key = api_key

    def sample(self, text, temperature=0.8, max_tokens=100):
        metadata = {"model": self.model_name,
                    "temperature": temperature,
                    "max_tokens": max_tokens}

        # sample from the openai model

        r = openai.ChatCompletion.create(
            messages=[
                {"role": "system", "content": "You are a search engine that replies to query based on context. Answer with "
                                              "information provided within the context otherwise reply with 'I don't know'"},
                {"role": "user", "content": text}
            ],
            **metadata
        )
        return r['choices'][0]["message"]["content"]

    def sample_many(self, prompts, max_workers=8):
        records = thread_map(self.sample, prompts, max_workers=max_workers)
        return [r for r in records]
