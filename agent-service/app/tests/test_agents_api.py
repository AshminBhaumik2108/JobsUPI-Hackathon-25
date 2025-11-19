import json
from unittest.mock import patch

from langchain_core.messages import AIMessage
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class DummyLLM:
    def invoke(self, prompt: str):
        if "rank the best 3 roles" in prompt:
            payload = [
                {
                    "role_id": "delivery-executive",
                    "title": "Delivery Executive",
                    "match_score": 0.8,
                    "rationale": "LLM match",
                }
            ]
            return AIMessage(content=[{"type": "text", "text": json.dumps(payload)}])
        return AIMessage(content=[{"type": "text", "text": "Delivery Executive fits well with a short roadmap."}])


@patch("app.graph.nodes.get_llm", return_value=DummyLLM())
def test_profile_endpoint_returns_normalized_data(mock_llm):
    payload = {
        "seeker_profile": {
            "skills": ["Inventory"],
            "personality": ["Detail-oriented"],
            "preferred_mobility": "low"
        }
    }
    response = client.post("/agents/profile", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "normalized_profile" in data
    assert data["normalized_profile"]["skills"] == ["inventory"]


@patch("app.graph.nodes.get_llm", return_value=DummyLLM())
def test_role_fit_endpoint_returns_candidates(mock_llm):
    payload = {
        "seeker_profile": {
            "skills": ["Transport", "Customer"],
            "personality": ["extrovert"],
        }
    }
    response = client.post("/agents/role-fit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["role_candidates"]
    assert data["selected_role_id"]


@patch("app.graph.nodes.get_llm", return_value=DummyLLM())
def test_roadmap_endpoint_can_email(mock_llm):
    payload = {
        "seeker_profile": {
            "skills": ["Transport"],
            "personality": [],
        },
        "email": "demo@example.com"
    }
    response = client.post("/agents/roadmap", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "roadmap" in data
    assert data["email_status"] in (None, "queued", "Gmail credentials missing; email skipped")
