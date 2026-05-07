from langchain.tools import tool

@tool
def mock_searxng_search(query: str) -> str:
    """
    Returns mocked news headlines based on keywords.
    """

    query = query.lower()

    if "crypto" in query:
        return (
            "Bitcoin hits new all-time high amid ETF approvals."
        )

    if "ai" in query:
        return (
            "OpenAI launches autonomous coding agent."
        )

    if "market" in query:
        return (
            "Federal Reserve hints at possible rate cuts."
        )

    if "space" in query:
        return (
            "SpaceX announces next-generation Mars mission timeline."
        )

    return (
        "Tech leaders debate the future of artificial intelligence."
    )