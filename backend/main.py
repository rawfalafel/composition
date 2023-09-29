import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import Union
from backend.agents import Developer, ProductOwner
from backend.project import get_project_json_path
from backend.project_types import AgentType, CodeChangeMessage, Composition, LogMessage, TextMessage

load_dotenv()
root_directory = os.getenv("ROOT_DIRECTORY")
project_json_path = get_project_json_path(root_directory)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def current_composition_state():
    with open(project_json_path, "r") as f:
        content = f.read()
        return Composition.model_validate_json(content)


@app.get("/workflow")
async def workflow():
    return current_composition_state()


def _get_agent(agent_type: AgentType):
    return {
        AgentType.PRODUCT_OWNER: ProductOwner(),
        AgentType.DEVELOPER: Developer()
    }[agent_type]


@app.post("/next")
async def next_message(user_message: Union[TextMessage, CodeChangeMessage]):
    # Get current state
    current_state = current_composition_state()

    agent = _get_agent(current_state.latest_step().agent)

    # Append to conversation
    current_state.latest_step().log.append(
        LogMessage(
            source="user",
            message=user_message
        )
    )

    async def process_response():
        collected_messages = []
        async for chunk in agent.stream_response(current_state):
            collected_messages.append(chunk)
            yield chunk;

        response = ''.join(m for m in collected_messages)
        current_state.latest_step().log.append(
            LogMessage(
                source="agent",
                message=TextMessage(text=response)
            )
        )

        with open(project_json_path, "w") as f:
            f.write(current_state.model_dump_json(indent=4))

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
        # return response

    return StreamingResponse(process_response(), media_type="text/plain")


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
