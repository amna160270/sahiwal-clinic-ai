from agents.base_agent import BaseAgent
from typing import Any, Dict


class RouterAgent(BaseAgent):
    """
    Router Agent classifies incoming queries into 'rag' or 'general' category.
    Inherits from BaseAgent and works with LangGraph State management.
    """

    def __init__(self):
        """Initialize the RouterAgent with classification system prompt."""
        system_prompt = """You are a Medical Query Router Assistant.
Your job is to analyze patient queries and classify them into one of these categories:
1. "rag" - Medical knowledge queries (symptoms, medicines, treatments, diseases, clinic services)
2. "general" - General conversation or non-medical queries

Respond with ONLY the category name: either "rag" or "general"."""

        super().__init__(name="RouterAgent", system_prompt=system_prompt)

        # Keywords for fast classification (fallback)
        self.rag_keywords = {
            "medicine", "symptom", "doctor", "treatment",
            "disease", "pain", "fever", "clinic", "appointment",
            "diagnosis", "medication", "health", "hospital",
            "prescription", "doctor", "patient", "surgery"
        }

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify the query and update state with query_type.
        LangGraph-compatible interface.

        Args:
            state: Current state from LangGraph

        Returns:
            Updated state with query_type field set
        """
        # Try intelligent classification first using LLM
        query_type = self._classify_with_llm(state.get("user_query", ""))

        # Fallback to keyword-based classification if needed
        if not query_type:
            query_type = self._classify_with_keywords(
                state.get("user_query", ""))

        # Update state
        state["query_type"] = query_type
        state["messages"].append(f"[Router] Classified as: {query_type}")

        return state

    def _classify_with_llm(self, query: str) -> str:
        """
        Use LLM to intelligently classify the query.

        Args:
            query: User query to classify

        Returns:
            Classification: "rag" or "general"
        """
        try:
            response = self.run(query)
            classification = response.strip().lower()

            # Validate response
            if classification in ["rag", "general"]:
                return classification

            # If LLM doesn't return expected format, fall back to keywords
            return ""
        except Exception as e:
            print(f"Error in LLM classification: {e}")
            return ""

    def _classify_with_keywords(self, query: str) -> str:
        """
        Fallback keyword-based classification.

        Args:
            query: User query to classify

        Returns:
            Classification: "rag" or "general"
        """
        query_lower = query.lower()

        # Check for RAG keywords
        if any(keyword in query_lower for keyword in self.rag_keywords):
            return "rag"

        # Default to general
        return "general"
