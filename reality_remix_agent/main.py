# reality_remix_agent/main.py
"""Orchestration graph."""

from langgraph.graph import StateGraph, END
from .agents import ideator_node, brancher_node, evaluator_node


def build_graph():
    """Builds the LangGraph workflow for the remix agent."""

    # State type is a dict; LangGraph will mutate and pass it along
    workflow = StateGraph(dict)

    # Register nodes
    workflow.add_node("ideator", ideator_node)
    workflow.add_node("brancher", brancher_node)
    workflow.add_node("evaluator", evaluator_node)

    # Connect nodes
    workflow.add_edge("ideator", "brancher")
    workflow.add_edge("brancher", "evaluator")
    workflow.add_edge("evaluator", END)

    # Entry point
    workflow.set_entry_point("ideator")

    # Compile workflow into an executable graph
    return workflow.compile()
