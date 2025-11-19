"""Factory for assembling the LangGraph pipeline used by the agent."""

from __future__ import annotations

from functools import lru_cache

from langgraph.graph import END, StateGraph

from app.graph.nodes import (
    collect_profile_node,
    roadmap_builder_node,
    role_scoring_node,
    summary_node,
)
from app.graph.state import SeekerGraphState


@lru_cache
def build_seeker_graph():
    """Compile and cache the seeker guidance LangGraph."""

    graph = StateGraph(SeekerGraphState)
    graph.add_node("collect_profile", collect_profile_node)
    graph.add_node("role_scoring", role_scoring_node)
    graph.add_node("roadmap_builder", roadmap_builder_node)
    graph.add_node("generate_summary", summary_node)

    graph.set_entry_point("collect_profile")
    graph.add_edge("collect_profile", "role_scoring")
    graph.add_edge("role_scoring", "roadmap_builder")
    graph.add_edge("roadmap_builder", "generate_summary")
    graph.add_edge("generate_summary", END)

    compiled_graph = graph.compile()
    return compiled_graph
