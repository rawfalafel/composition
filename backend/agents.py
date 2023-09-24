import os
from enum import Enum
from abc import ABC
from pydantic import BaseModel
from dotenv import load_dotenv
import openai


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
print(OPENAI_API_KEY)

def _generate_chat_history():
    pass


def contact_openai(chat_history) -> str:
    return openai.ChatCompletion.create(
        model="gpt-4", messages=chat_history, stream=True
    )


class Agent(BaseModel, ABC):
    def stream_response(self, composition):
        raise NotImplementedError()


class ProductOwner(Agent):
    async def stream_response(self, composition):
        last_message = composition.latest_step().log[-1]
        response = contact_openai([
            {"role": "user", "content": last_message.message.text}
        ])

        for chunk in response:
            delta = chunk['choices'][0]['delta']
            if 'content' in delta:
                yield(delta.content)

        

class Developer(Agent):
    pass


class AgentType(str, Enum):
    PRODUCT_OWNER = "PRODUCT_OWNER"
    DEVELOPER = "DEVELOPER"
