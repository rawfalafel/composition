from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union


class CodeChangeMessage(BaseModel):
    file_name: str
    old_code: str
    new_code: str


class TextMessage(BaseModel):
    text: str


class LogMessage(BaseModel):
    source: str
    message: Union[TextMessage, CodeChangeMessage]


class WorkflowStep(BaseModel):
    agent: str
    log: List[LogMessage]


class Composition(BaseModel):
    agents: List[str]
    workflow: List[WorkflowStep]


app = FastAPI()


@app.get("/workflow")
async def workflow():
    with open("project.json", "r") as f:
        content = f.read()

        print(content)
        return Composition.model_validate_json(content)


@app.get("/next")
async def index():
    # This accepts an "Update" json object, and updates the full state
    # in memory & on disk.

    # {"data": " "}

    # {"" }
    return {"message": "Hello World"}


#
# """
# JSON object example:
#
# {
#     "agents": [
#         {"product"}
#     ]
#     steps: [
#         {
#             "agent": "product-owner",
#             "conversation": [
#                 { }, // messages (agent or user)
#             ]
#         },
#     ],
#
#
#
#
#}
#
#1. What are first-class features?
#2. 
#
#
#
#Agent Schema:
#
# * what do we need to be able to express here?
#     *  What to ask the user for? (this is not one thing, could be series of questions)
#     *  What to ask OpenAI for?
#     *  How to process the 
#
#
#     * What is the interface to an agent? It has some conversation state, and figures out when it's done.
#     * Outputs next text -- and then takes the user input
#
#
# product_owner.json:
#
# {
# 
#
# } 
#
#"""