"""
This module implements the Phase 2 graph logic for the Cognitive Routing RAG system,
"""

from langgraph.graph import StateGraph, END

from app.models import GraphState, SearchDecision, BotPost
from app.tools import mock_searxng_search
from app.utils import get_llm

llm = get_llm()

#Node 1: Decide Search
planner_llm = llm.with_structured_output(SearchDecision, method="json_mode")

def decide_search(graph_state: GraphState):
    """
    This node decides on a topic to post about and 
    whether to perform a web search based on the bot's persona.
    """
    prompt = f"""
            You are roleplaying the following persona:

            {graph_state["persona"]}

            Choose a topic this bot wants to post about today.

            Generate:
            1. A concise topic
            2. A concise web search query

            Return valid JSON only.
            """
    result = planner_llm.invoke(prompt)
    return {"topic": result.topic,
            "search_query": result.search_query}

#Node 2: Dummy web Search
def web_search(state: GraphState):
    """
    This node performs a <dummy> web search based on the search query.
    """
    result = mock_searxng_search.invoke(
        state["search_query"]
    )
    return {
        "search_results": result
    }

#Node 3: Draft Post
writer_llm = llm.with_structured_output(
    BotPost, method="json_mode"
)

def draft_post(state: GraphState):
    """
    This node drafts a social media post based 
     - bot's persona
     - the chosen topic
     - web search results.
    """
    prompt = f"""
    You are permanently roleplaying this persona:

    {state["persona"]}

    You are reacting to this real-world news:

    {state["search_results"]}

    Topic:
    {state["topic"]}

    Requirements:
    - Strongly reference the news/context
    - Sound like a real human with strong beliefs
    - Stay highly aligned to the persona
    - Under 280 characters
    - No hashtags
    - No emojis
    - Avoid generic motivational language
    - Make a concrete argument or prediction
    - Don't just state an opinion, but also provide reasoning or evidence for it

    Return a valid JSON object with exactly one key: "post_content".
    Do not wrap it in markdown or code fences.
    Example: {{"post_content": "..."}}
    """
    result = writer_llm.invoke(prompt)
    return {
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

def phase2_demo():
    """
    This function demonstrates the phase 2 graph logic.
    """
    from app.personas import BOT_PERSONAS
    output = {}
    for i in BOT_PERSONAS:
        initial_state = {
        "bot_id": i["bot_id"],
        "persona": i["persona"]
        }
        result = graph.invoke(initial_state)
        final_output = {
            "bot_id": result["bot_id"],
            "topic": result["topic"],
            "post_content": result["post_content"]
        }
        output[i['bot_id']] = final_output
    return output

if __name__ == "__main__":
    from pprint import pprint
    pprint(phase2_demo())
