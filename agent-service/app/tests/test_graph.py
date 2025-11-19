import json
from unittest.mock import patch

from langchain_core.messages import AIMessage

from app.graph import build_seeker_graph


class DummyLLM:
    def invoke(self, prompt: str):
        if "rank the best 3 roles" in prompt:
            payload = [
                {
                    "role_id": "warehouse-associate",
                    "title": "Warehouse Associate",
                    "match_score": 0.9,
                    "rationale": "Fits skills and preferences",
                }
            ]
            return AIMessage(content=[{"type": "text", "text": json.dumps(payload)}])

        summary_text = "Warehouse Associate suits the seeker with a 4-week roadmap."
        return AIMessage(content=[{"type": "text", "text": summary_text}])


@patch("app.graph.nodes.get_llm", return_value=DummyLLM())
def test_graph_generates_recommendations(mock_llm):
    graph = build_seeker_graph()
    state = graph.invoke(
        {
            "seeker_profile": {
                "skills": ["inventory", "transport"],
                "personality": ["detail-oriented"],
                "preferred_mobility": "low",
            }
        }
    )

    assert state["role_candidates"], "Expected at least one recommendation"
    assert state["summary"].startswith("Warehouse Associate")
    assert state["roadmap"], "Roadmap should be generated"


@patch("app.graph.nodes.get_llm", return_value=DummyLLM())
def test_graph_handles_missing_profile(mock_llm):
    graph = build_seeker_graph()
    state = graph.invoke({"seeker_profile": {}})

    assert "errors" in state
    combined_errors = " ".join(state["errors"])
    assert "Profile inputs missing" in combined_errors or "Unable" in combined_errors
