from typing import TypedDict
from pydantic import AliasChoices, BaseModel, Field

class GraphState(TypedDict):
    bot_id: str
    persona: str

    topic: str
    search_query: str
    search_results: str

    post_content: str

class SearchDecision(BaseModel):
    topic: str
    search_query: str = Field(
        validation_alias=AliasChoices("search_query", "webSearchQuery", "web_search_query")
    )

class BotPost(BaseModel):
    post_content: str = Field(
        validation_alias=AliasChoices("post_content", "text", "content")
    )
