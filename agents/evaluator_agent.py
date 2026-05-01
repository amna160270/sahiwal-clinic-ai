from agents.base_agent import BaseAgent


class EvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="EvaluatorAgent",
            system_prompt="""You are a quality checker for a medical clinic AI assistant.
Check if the response:
1. Actually answers the patient's question
2. Is polite and professional
3. Does not contain harmful medical advice

Reply with ONLY one word: 'pass' or 'fail'. Nothing else."""
        )

    def evaluate(self, state):
        query = state["user_query"]
        response = state["agent_response"]
        prompt = f"Patient Question: {query}\nAI Response: {response}\n\nIs this response good?"
        result = self.run(prompt).strip().lower()
        if result not in ["pass", "fail"]:
            result = "pass"
        print(f"🔍 Evaluator: {result.upper()}")
        return {"evaluation_result": result}
