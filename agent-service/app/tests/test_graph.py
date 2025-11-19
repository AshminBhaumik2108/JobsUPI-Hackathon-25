from app.graph import build_seeker_graph


def test_graph_generates_recommendations():
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
    assert state["summary"].startswith("Recommended role")
    assert state["roadmap"], "Roadmap should be generated"


def test_graph_handles_missing_profile():
    graph = build_seeker_graph()
    state = graph.invoke({"seeker_profile": {}})

    assert "errors" in state
    combined_errors = " ".join(state["errors"])
    assert "Profile inputs missing" in combined_errors or "Unable" in combined_errors
