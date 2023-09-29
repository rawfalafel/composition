from abc import ABC
from pydantic import BaseModel
import openai
from backend.agent_processing import convert_messages_format

from backend.openai import QUERY_MODEL, setup_openai

setup_openai()

def _generate_chat_history():
    pass


def contact_openai(messages) -> str:
    return openai.ChatCompletion.create(
        model=QUERY_MODEL, messages=messages, stream=True
    )


class Agent(BaseModel, ABC):
    def stream_response(self, composition):
        raise NotImplementedError()


class ProductOwner(Agent):
    async def stream_response(self, composition):
        messages = convert_messages_format(composition.latest_step().log)
        response = contact_openai(messages)

        for chunk in response:
            delta = chunk['choices'][0]['delta']
            if 'content' in delta:
                yield(delta.content)

        

class Developer(Agent):
    pass

