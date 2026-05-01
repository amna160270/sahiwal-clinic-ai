from agents.base_agent import BaseAgent


class GeneralAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="GeneralAgent",
            system_prompt="""You are a friendly receptionist at Sahiwal Medical Clinic.
For greetings, respond warmly and ask how you can help.
For unrelated questions, politely say you can only help with clinic-related queries.
Keep responses short and friendly. You can speak Urdu or English."""
        )

    def respond(self, state):
        query = state["user_query"]
        response = self.run(query)
        print(f"💬 General Agent: Respond kar diya")
        return {"agent_response": response}
