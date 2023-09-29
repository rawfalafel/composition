from enum import Enum
from typing import List, Literal, Union
from pydantic import BaseModel

class CodeChangeMessage(BaseModel):
    file_name: str
    old_code: str
    new_code: str

class TextMessage(BaseModel):
    text: str

class LogMessage(BaseModel):
    source: Literal["user", "agent"]
    message: Union[TextMessage, CodeChangeMessage]

class AgentType(str, Enum):
    PRODUCT_OWNER = "PRODUCT_OWNER"
    DEVELOPER = "DEVELOPER"

class WorkflowStep(BaseModel):
    agent: AgentType
    log: List[LogMessage]


class Composition(BaseModel):
    agents: List[AgentType]
    workflow: List[WorkflowStep]

    def latest_step(self):
        return self.workflow[-1]