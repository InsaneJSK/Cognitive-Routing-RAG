"""
This module contains utility functions for initializing the LLM used in the RAG system.
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_llm(model = "llama-3.1-8b-instant", temperature=0.7):
    """
    Initializes and returns a ChatGroq LLM instance with specified parameters.
    """
    return ChatGroq(
        model=model,
        temperature=temperature,
    )
