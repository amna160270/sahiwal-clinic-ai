from agents.base_agent import BaseAgent


class RAGAgent(BaseAgent):
    def __init__(self, rag_tool):
        super().__init__(
            name="RAGAgent",
            system_prompt="""You are a helpful assistant for Sahiwal Medical Clinic.
Answer the patient's question using ONLY the context provided below.
If the answer is not in the context, say: 'Is baare mein mujhe maloomat nahi, please 0300-1234567 par call karein.'
Be polite and clear. You can respond in Urdu or English."""
        )
        self.rag_tool = rag_tool

    def answer(self, state):
        query = state["user_query"]
        print(f"📄 RAG Agent: Documents search kar raha hai...")
        context = self.rag_tool.retrieve(query)
        prompt = f"Clinic Documents:\n{context}\n\nPatient Question: {query}"
        response = self.run(prompt)
        print(f"✅ RAG Agent: Jawab mil gaya")
        return {
            "retrieved_context": context,
            "agent_response": response
        }
