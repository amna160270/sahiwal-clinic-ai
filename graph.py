from langgraph.graph import StateGraph, END
from typing import TypedDict

from agents.router_agent import RouterAgent
from agents.rag_agent import RAGAgent
from agents.general_agent import GeneralAgent
from agents.evaluator_agent import EvaluatorAgent
from tools.rag_tool import RAGTool


class AgentState(TypedDict):
    user_query: str
    query_type: str
    retrieved_context: str
    agent_response: str
    evaluation_result: str
    final_response: str
    retry_count: int


def build_graph():
    rag_tool = RAGTool()
    rag_tool.load_and_index()

    router = RouterAgent()
    rag_agent = RAGAgent(rag_tool)
    general_agent = GeneralAgent()
    evaluator = EvaluatorAgent()

    def router_node(state):
        return router.route(state)

    def rag_node(state):
        return rag_agent.answer(state)

    def general_node(state):
        return general_agent.respond(state)

    def evaluator_node(state):
        return evaluator.evaluate(state)

    def final_node(state):
        return {"final_response": state["agent_response"]}

    def route_query(state):
        return state["query_type"]

    def check_evaluation(state):
        retry = state.get("retry_count", 0)
        if state["evaluation_result"] == "fail" and retry < 1:
            return "retry"
        return "done"

    builder = StateGraph(AgentState)

    builder.add_node("router", router_node)
    builder.add_node("rag_agent", rag_node)
    builder.add_node("general_agent", general_node)
    builder.add_node("evaluator", evaluator_node)
    builder.add_node("final", final_node)

    builder.set_entry_point("router")

    builder.add_conditional_edges("router", route_query, {
        "rag": "rag_agent",
        "general": "general_agent"
    })

    builder.add_edge("rag_agent", "evaluator")
    builder.add_edge("general_agent", "evaluator")

    builder.add_conditional_edges("evaluator", check_evaluation, {
        "retry": "rag_agent",
        "done": "final"
    })

    builder.add_edge("final", END)

    return builder.compile()
