from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum
from typing import List, Union, Literal
from backend.agents import Agent

class CodeChangeMessage(BaseModel):
    file_name: str
    old_code: str
    new_code: str


class TextMessage(BaseModel):
    text: str


class LogMessage(BaseModel):
    source: Literal["user", "agent"]
    message: Union[TextMessage, CodeChangeMessage]


class WorkflowStep(BaseModel):
    agent: Agent
    log: List[LogMessage]


class Composition(BaseModel):
    agents: List[Agent]
    workflow: List[WorkflowStep]

    def latest_step(self):
        return self.workflow[-1]


app = FastAPI()

origins = [ "http://localhost:3000" ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def current_composition_state():
    with open("project.json", "r") as f:
        content = f.read()
        return Composition.model_validate_json(content)


@app.get("/workflow")
async def workflow():
    return current_composition_state()


@app.post("/next")
async def next_message(user_message: Union[TextMessage, CodeChangeMessage]):
    # Get current state
    current_state = current_composition_state()

    # Append to conversation
    current_state.latest_step().log.append(
        LogMessage(
            source="user",
            message=user_message
        )
    )

    with open("project.json", "w") as f:
        f.write(current_state.model_dump())

    # Generate next action to take from the current agent


    # Save to disk
    # Return current conversation



    # Todo:
        # 1. Load the current state from disk (maybe it should already
    #        be in memory
        # 2. Append the new message to the conversation
        #     
    # This accepts an "Update" json object, and updates the full state
    # in memory & on disk.

    # {"data": " "}

    # {"" }
    return current_state


@app.post("/approve")
def approve():
    pass


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