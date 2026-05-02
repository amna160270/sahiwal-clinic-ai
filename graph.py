import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from agents.router_agent import RouterAgent
from agents.rag_agent import RAGAgent
from agents.general_agent import GeneralAgent
from agents.evaluator_agent import EvaluatorAgent

from langchain_groq import ChatGroq
from knowledge_base.kb import MedicalKnowledgeBase

# Load environment variables
load_dotenv()


# =========================
# 🧠 LLM SETUP (Secure)
# =========================
def get_llm():
    """Initialize LLM with secure API key from environment."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")

    return ChatGroq(
        api_key=api_key,
        model="llama-3.1-8b-instant",
        temperature=0.3
    )


llm = get_llm()


# =========================
# 🧠 KNOWLEDGE BASE
# =========================
kb = MedicalKnowledgeBase()
kb.build_db("data/medical.txt")


# =========================
# 🧠 STATE DEFINITION
# =========================
class State(TypedDict):
    user_query: str
    query_type: str
    retrieved_context: str
    agent_response: str
    evaluation_result: str
    final_response: str
    messages: List[BaseMessage]


# =========================
# 🧠 AGENT INITIALIZATION
# =========================
router = RouterAgent()
rag = RAGAgent(llm, kb)
general = GeneralAgent()
evaluator = EvaluatorAgent()


# =========================
# 🔹 GRAPH NODES
# =========================

def router_node(state: State) -> State:
    """Route query to either RAG or General agent."""
    state = router.invoke(state)
    return state


def rag_node(state: State) -> State:
    """Process query using RAG (Retrieval-Augmented Generation)."""
    state = rag.invoke(state)
    return state


def general_node(state: State) -> State:
    """Process query using General Agent for non-medical queries."""
    state = general.invoke(state)

    return state


def evaluator_node(state: State) -> State:
    """Evaluate the agent response for quality and accuracy."""
    result = evaluator.check(state["agent_response"])

    state["evaluation_result"] = result

    if result == "fail":
        state["final_response"] = "⚠ Response quality check failed. Please rephrase or ask another question."
    else:
        state["final_response"] = state["agent_response"]

    state["messages"].append(AIMessage(content=state["final_response"]))

    return state


# =========================
# 🔹 ROUTING LOGIC
# =========================

def route_decision(state: State) -> str:
    """Conditional routing based on query classification."""
    return state["query_type"]


# =========================
# 🔹 GRAPH CONSTRUCTION
# =========================

graph = StateGraph(State)

# Add nodes
graph.add_node("router", router_node)
graph.add_node("rag", rag_node)
graph.add_node("general", general_node)
graph.add_node("evaluator", evaluator_node)

# Set entry point
graph.set_entry_point("router")

# Add conditional edges (routing)
graph.add_conditional_edges(
    "router",
    route_decision,
    {
        "rag": "rag",
        "general": "general"
    }
)

# Add edges to evaluator and end
graph.add_edge("rag", "evaluator")
graph.add_edge("general", "evaluator")
graph.add_edge("evaluator", END)

# Compile the graph
app = graph.compile()
