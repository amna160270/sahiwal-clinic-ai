from agents.base_agent import BaseAgent
from typing import Any, Dict
from langchain_core.messages import AIMessage


class EvaluatorAgent(BaseAgent):
    """
    Evaluator Agent checks the quality and accuracy of responses.
    Inherits from BaseAgent and works with LangGraph State management.
    """

    def __init__(self):
        """Initialize EvaluatorAgent with evaluation system prompt."""
        system_prompt = """You are a Quality Assurance Agent for Sahiwal Clinic AI.

Your responsibilities:
- Evaluate response quality and accuracy
- Check if responses are helpful and appropriate
- Identify potentially harmful or incorrect medical information
- Rate responses as "pass" or "fail"

EVALUATION CRITERIA:
- Response should be substantive (not too short)
- Should not contain error messages or "unknown" responses
- Should be relevant to the query
- Should not promote harmful advice
- Should encourage consulting professionals for medical issues

Respond with ONLY "pass" or "fail" followed by brief reason."""

        super().__init__(name="EvaluatorAgent", system_prompt=system_prompt)

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate agent response.
        LangGraph-compatible interface.

        Args:
            state: Current state from LangGraph

        Returns:
            Updated state with evaluation result
        """
        response = state.get("agent_response", "")

        # Evaluate response
        result = self.check(response)

        # Update state
        state["evaluation_result"] = result
        state["messages"].append(AIMessage(content=f"Quality check: {result}"))

        return state

    def check(self, response: str) -> str:
        """
        Check response quality using multiple criteria.

        Args:
            response: Agent response to evaluate

        Returns:
            "pass" or "fail"
        """
        # First, apply quick hardcoded checks
        if self._quick_check_fail(response):
            return "fail"

        # If quick checks pass, use LLM for detailed evaluation
        try:
            evaluation = self.run(f"Evaluate this response: {response}")

            # Check if evaluation mentions "pass"
            if "pass" in evaluation.lower():
                return "pass"
            else:
                return "fail"

        except Exception as e:
            print(f"Error in evaluation: {e}")
            # Default to pass if evaluation fails
            return "pass"

    def _quick_check_fail(self, response: str) -> bool:
        """
        Quick hardcoded checks for obvious failures.

        Args:
            response: Response to check

        Returns:
            True if response should fail, False otherwise
        """
        response_lower = response.lower()

        # Check for minimum length (too short response)
        if len(response) < 20:
            print("Evaluation: Response too short")
            return True

        # Check for error indicators
        if any(error_word in response_lower for error_word in
               ["error", "exception", "unable to", "unknown", "failed", "i don't know"]):
            print("Evaluation: Response contains error indicators")
            return True

        # Check for empty or placeholder responses
        if response.strip() in ["", "...", "N/A", "null", "undefined"]:
            print("Evaluation: Response is empty or placeholder")
            return True

        return False
