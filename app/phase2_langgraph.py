from langgraph.graph import StateGraph, END

from app.models import GraphState, SearchDecision, BotPost
from app.tools import mock_searxng_search
from app.utils import get_llm

llm = get_llm()

#Node 1: Decide Search
planner_llm = llm.with_structured_output(SearchDecision)

def decide_search(graph_state: GraphState):
    prompt = f"""
            You are roleplaying the following persona:

            {graph_state["persona"]}

            Choose a topic this bot wants to post about today.

            Generate:
            1. A concise topic
            2. A concise web search query
            """
    result = planner_llm.invoke(prompt)
    return {"topic": result.topic,
            "search_query": result.search_query}

#Node 2: Dummy web Search
def web_search(state: GraphState):
    result = mock_searxng_search.invoke(
        state["search_query"]
    )
    return {
        "search_results": result
    }

#Node 3: Draft Post
writer_llm = llm.with_structured_output(
    BotPost
)
def draft_post(state: GraphState):
    prompt = f"""
    You are roleplaying the following persona:
    {state["persona"]}

    Use this real-world context:
    {state["search_results"]}

    Write:
    - a highly opinionated social media post
    - under 280 characters
    - aggressive and confident
    - strongly aligned to the persona

    Return valid JSON only.
    """
    result = writer_llm.invoke(prompt)
    return {
        "bot_id": state["bot_id"],
        "topic": state["topic"],
        "post_content": result.post_content
    }

#Graph Construction
builder = StateGraph(GraphState)

builder.add_node(
    "decide_search",
    decide_search
)

builder.add_node(
    "web_search",
    web_search
)

builder.add_node(
    "draft_post",
    draft_post
)

builder.set_entry_point(
    "decide_search"
)

builder.add_edge(
    "decide_search",
    "web_search"
)

builder.add_edge(
    "web_search",
    "draft_post"
)

builder.add_edge(
    "draft_post",
    END
)

graph = builder.compile()

if __name__ == "__main__":
    initial_state = {
    "bot_id": "Bot_A",
    "persona": (
        "I believe AI and crypto will solve "
        "all human problems..."
    )}
    result = graph.invoke(initial_state)
    print(result)
