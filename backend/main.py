from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from enum import Enum
from typing import List, Union, Literal
from backend.agents import AgentType, Developer, ProductOwner
from backend.watchfiles import list_files_in_directory, save_file_list

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
    agent: AgentType
    log: List[LogMessage]


class Composition(BaseModel):
    agents: List[AgentType]
    workflow: List[WorkflowStep]

    def latest_step(self):
        return self.workflow[-1]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

        with open("project.json", "w") as f:
            f.write(current_state.model_dump_json())

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

# Example usage
root_directory = '/Users/yutaro/code/orca-2'  # Replace this with the actual root directory path
file_list = list_files_in_directory(root_directory)
save_file_list(file_list, root_directory)

# Print the list of files
try:
    for file_path in file_list:
        print(file_path)
except Exception as e:
    print(f"An exception occurred: {e}")


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
