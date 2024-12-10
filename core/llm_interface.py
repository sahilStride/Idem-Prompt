import os,openai
from openai import OpenAI
import random
import time
from functools import wraps
from dataclasses import dataclass, field
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def retry_with_exponential_backoff(
    func,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 3,
    errors: tuple = (openai.RateLimitError, openai.APIError),
):
    """Retry a function with exponential backoff."""
    def wrapper(*args, **kwargs):
        num_retries = 0
        delay = initial_delay
        while True:
            try:
                return func(*args, **kwargs)
            except errors as e:
                num_retries += 1
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )
                delay *= exponential_base * (1 + jitter * random.random())
                time.sleep(delay)
            except Exception as e:
                raise e
    return wrapper

@retry_with_exponential_backoff
def openai_chat_completion(**kwargs):
    return client.chat.completions.create(**kwargs)

@dataclass
class Prompt:
    user_prompt: Optional[str] = None
    system: Optional[str] = None
    messages: Optional[List] = None
    model: str = "gpt-4o-mini"
    kwargs: dict = field(default_factory=dict)

def create_message_list(prompt: Prompt):
    messages = []
    if prompt.system:
        messages.append({"role": "system", "content": prompt.system})
    if prompt.messages:
        messages.extend(prompt.messages)
    if prompt.user_prompt:
        messages.append({"role": "user", "content": prompt.user_prompt})
    return messages

def create_and_send_prompt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        prompt = func(*args, **kwargs)
        model = "gpt-4o-mini"
        kwargs = {
            "temperature": 0.0,
            "top_p": 1,
            "seed": 1234,
            "n":1,
            "frequency_penalty":0,
            "presence_penalty":0
        }
        if isinstance(prompt, Prompt):
            messages = create_message_list(prompt)
            model = prompt.model
            kwargs.update(prompt.kwargs)
        else:
            raise ValueError(
                "Returned value must be a string or emergent.Prompt object"
            )
        response = openai_chat_completion(
            model=model,
            messages=messages,
            **kwargs,
        )
        return response.choices[0].message.content
    return wrapper