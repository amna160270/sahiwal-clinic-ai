from agents.base_agent import BaseAgent
from typing import Any, Dict
import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage

load_dotenv()


class GeneralAgent(BaseAgent):
    """
    General Agent for non-medical queries and general conversation.
    Inherits from BaseAgent and works with LangGraph State management.
    """

    def __init__(self):
        """Initialize GeneralAgent with general conversation system prompt."""
        system_prompt = """You are a helpful AI assistant for Sahiwal Clinic.

Your responsibilities:
- Handle general questions and casual conversation
- Support both English and Roman Urdu (Pakistani style)
- Be friendly and helpful
- Direct medical questions to appropriate medical resources
- Provide basic clinic information

IMPORTANT RULES:
- If user writes in Urdu/Roman Urdu → reply in Roman Urdu
- If user writes in English → reply in English
- For medical questions, suggest visiting the clinic or consulting a doctor
- Keep responses friendly and concise"""

        super().__init__(name="GeneralAgent", system_prompt=system_prompt)

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process general query.
        LangGraph-compatible interface.

        Args:
            state: Current state from LangGraph

        Returns:
            Updated state with agent response
        """
        query = state.get("user_query", "")

        # Generate response for general query
        response = self.respond(query)

        # Update state
        state["agent_response"] = response
        state["messages"].append(AIMessage(content=response))

        return state

    def respond(self, query: str) -> str:
        """
        Generate response to general query.

        Args:
            query: User query

        Returns:
            Generated response
        """
        try:
            # Special handling for doctor queries
            if any(keyword in query.lower() for keyword in ["doctor", "clinic", "appointment", "timings"]):
                return self._handle_clinic_query(query)

            # General conversation
            response = self.run(query)
            return response.strip()

        except Exception as e:
            print(f"Error in general response: {e}")
            return "I'm sorry, I couldn't process your request. Please try again."

    def _handle_clinic_query(self, query: str) -> str:
        """
        Handle clinic-specific questions.

        Args:
            query: User query

        Returns:
            Clinic information response
        """
        query_lower = query.lower()

        if "doctor" in query_lower or "consultant" in query_lower:
            return """🏥 Hamaray qualified doctors available hain:
- General Practitioner (Monday-Friday: 9 AM - 5 PM)
- Specialist consultation (By appointment)

Appointment ke liye contact karein: 0333-XXX-XXXX"""

        elif "appointment" in query_lower or "book" in query_lower:
            return """📞 Appointment booking:
- Phone: 0333-XXX-XXXX
- Visit clinic directly
- Khud sa aaen ya call karen"""

        elif "timing" in query_lower or "hours" in query_lower:
            return """🕐 Clinic Timings:
- Monday to Friday: 9 AM - 5 PM
- Saturday: 10 AM - 2 PM
- Sunday: Closed"""

        else:
            return self.run(query)
