from pydantic import BaseModel

class LLMItem(BaseModel):
    query: str

