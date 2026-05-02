from agents.base_agent import BaseAgent
from typing import Any, Dict
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage


class RAGAgent(BaseAgent):
    """
    RAG (Retrieval-Augmented Generation) Agent for medical queries.
    Retrieves context from knowledge base and generates informed responses.
    Inherits from BaseAgent and works with LangGraph State management.
    """

    def __init__(self, llm: ChatGroq, kb: Any):
        """
        Initialize RAGAgent with knowledge base.

        Args:
            llm: ChatGroq instance
            kb: MedicalKnowledgeBase instance
        """
        system_prompt = """You are a professional medical AI assistant for Sahiwal Clinic.

Your responsibilities:
- Answer medical questions using ONLY the provided context
- Support both English and Roman Urdu (Pakistani style)
- Use simple, easy-to-understand language
- Never provide medical diagnoses - suggest consulting a doctor
- Format responses with clear sections

IMPORTANT RULES:
- If user writes in Urdu/Roman Urdu → reply in Roman Urdu
- If user writes in English → reply in English
- Use only simple words from the given context
- Avoid Hindi words (sampark, adhik, sharminda, aavashyak)
- Keep answers concise and helpful"""

        super().__init__(name="RAGAgent", system_prompt=system_prompt)
        self.kb = kb
        self.llm = llm  # Override with provided LLM

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process medical query using RAG pattern.
        LangGraph-compatible interface.

        Args:
            state: Current state from LangGraph

        Returns:
            Updated state with retrieved context and response
        """
        query = state.get("user_query", "")

        # Step 1: Retrieve relevant context from knowledge base
        context = self.retrieve(query)

        # Step 2: Generate response using retrieved context
        response = self.generate(query, context)

        # Step 3: Update state
        state["retrieved_context"] = context
        state["agent_response"] = response
        state["messages"].append(
            AIMessage(content=f"[RAG] Retrieved context and generated response"))

        return state

    def retrieve(self, query: str) -> str:
        """
        Retrieve relevant context from knowledge base using FAISS.

        Args:
            query: User query to search for

        Returns:
            Retrieved context from knowledge base
        """
        try:
            # Search knowledge base (FAISS)
            results = self.kb.search(query, top_k=3)

            if not results:
                return "No relevant information found in knowledge base. Please consult a doctor."

            # Format results
            context = "\n".join([f"- {result}" for result in results])
            return context

        except Exception as e:
            print(f"Error retrieving context: {e}")
            return "Unable to retrieve information. Please try again."

    def generate(self, query: str, context: str) -> str:
        """
        Generate response based on query and retrieved context.

        Args:
            query: User query
            context: Retrieved context from knowledge base

        Returns:
            Generated response
        """
        prompt = f"""Based on the following context, answer the user's question.

Context:
{context}

User Question:
{query}

Please provide a helpful, accurate response in the same language as the user's question.
If information is not in the context, say so clearly."""

        try:
            response = self.run(prompt)

            # Clean response (remove Hindi words)
            bad_words = ["sampark", "adhik", "sharminda", "aavashyak"]
            for word in bad_words:
                response = response.replace(word, "")

            return response.strip()

        except Exception as e:
            print(f"Error generating response: {e}")
            return "Unable to generate response. Please try again."
