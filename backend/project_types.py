from enum import Enum
from typing import List, Literal
from pydantic import BaseModel

from backend.embedding_types import EmbeddingRecord


class CodeChangeMessage(BaseModel):
    file_name: str
    old_code: str
    new_code: str


class TextMessage(BaseModel):
    text: str


class TextMessageWithContext(TextMessage):
    context: List[EmbeddingRecord]


Message = TextMessage | TextMessageWithContext | CodeChangeMessage


class LogMessage(BaseModel):
    source: Literal["user", "agent"]
    message: Message


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
