from agents.base_agent import BaseAgent


class RouterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="RouterAgent",
            system_prompt="""You are a query classifier for Sahiwal Medical Clinic.
Classify the user query into exactly one category:
- 'rag' : questions about doctors, appointments, medicines, clinic timings, diseases, fees, policies
- 'general' : greetings, thank you, unrelated questions

Reply with ONLY one word: 'rag' or 'general'. Nothing else."""
        )

    def route(self, state):
        query = state["user_query"]
        result = self.run(query).strip().lower()
        if result not in ["rag", "general"]:
            result = "rag"
        print(f"\n🔀 Router Decision: {result.upper()}")
        return {"query_type": result}
