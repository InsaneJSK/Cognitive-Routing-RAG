"""
This module defines the data models used in the application, 
including the structure of the graph state and the expected outputs from the writer LLM.
"""

from typing import TypedDict
from pydantic import AliasChoices, BaseModel, Field

class GraphState(TypedDict):
    """Defines the state of the graph at any point in time."""
    bot_id: str
    persona: str

    topic: str
    search_query: str
    search_results: str

    post_content: str

class SearchDecision(BaseModel):
    """Defines the expected output from the writer LLM when deciding to perform a web search."""
    topic: str
    search_query: str = Field(
        validation_alias=AliasChoices("search_query", "webSearchQuery", "web_search_query")
    )

class BotPost(BaseModel):
    """Defines the expected output from the writer LLM when generating a post."""
    post_content: str = Field(
        validation_alias=AliasChoices("post_content", "text", "content")
    )
