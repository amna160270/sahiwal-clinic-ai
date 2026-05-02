from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Any, Dict
import os
from dotenv import load_dotenv

load_dotenv()


class BaseAgent:
    """
    Base class for all agents in the Multi-Agent system.
    Designed to work seamlessly with LangGraph State management.
    """

    def __init__(self, name: str, system_prompt: str):
        """
        Initialize the BaseAgent.

        Args:
            name: Agent identifier
            system_prompt: System instructions for the agent
        """
        self.name = name
        self.system_prompt = system_prompt

        # Initialize LLM with secure API key from environment
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=api_key,
            temperature=0.3
        )

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a query using the agent.
        This is the LangGraph-compatible interface.

        Args:
            state: Current state from LangGraph

        Returns:
            Updated state dictionary
        """
        user_query = state.get("user_query", "")

        # Build conversation history from messages
        messages = [SystemMessage(content=self.system_prompt)]

        # Add previous messages if they exist
        if state.get("messages"):
            messages.extend(state["messages"])

        # Add current query
        messages.append(HumanMessage(content=user_query))

        # Get response from LLM
        response = self.llm.invoke(messages)
        response_text = response.content

        # Update state (to be overridden by subclasses for specific fields)
        state["messages"].append(HumanMessage(content=user_query))
        state["messages"].append(response)

        return state

    def run(self, user_message: str) -> str:
        """
        Simple wrapper for direct agent invocation (non-LangGraph mode).

        Args:
            user_message: User query

        Returns:
            Agent response
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_message)
        ]
        response = self.llm.invoke(messages)
        return response.content

    def __repr__(self) -> str:
        return f"{self.name}(Agent)"
