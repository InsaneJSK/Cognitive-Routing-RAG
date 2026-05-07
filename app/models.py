from typing import TypedDict
from pydantic import BaseModel

class GraphState(TypedDict):
    bot_id: str
    persona: str

    topic: str
    search_query: str
    search_results: str

    post_content: str

class SearchDecision(BaseModel):
    topic: str
    search_query: str

class BotPost(BaseModel):
    bot_id: str
    topic: str
    post_content: str
