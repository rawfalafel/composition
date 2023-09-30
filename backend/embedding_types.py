from typing import List
from pydantic import BaseModel

class EmbeddingRecord(BaseModel):
    file_path: str
    chunk_index: int
    content: str
    embedding: List[float]