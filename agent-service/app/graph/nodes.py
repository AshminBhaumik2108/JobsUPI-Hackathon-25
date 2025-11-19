"""LangGraph node implementations with inline error handling and logging."""

from __future__ import annotations

import json
from typing import Dict, List

from langchain_core.messages import AIMessage
from langsmith import traceable

from loguru import logger

from app.graph.state import RoadmapStep, RoleRecommendation, SeekerGraphState
from app.services.llm import get_llm

# Placeholder catalog data until the core-service API is wired in.
ROLE_LIBRARY: List[Dict] = [
    {
        "role_id": "mern-support-intern",
        "title": "MERN Support Intern",
        "skills": {"must_have": {"javascript": 1, "html": 1}, "nice_to_have": {"mongodb": 1}},
        "personality": ["detail-oriented", "curious"],
        "environment": {"mobility": "low"},
        "roadmap": [
            {
                "title": "Frontend refresh",
                "description": "Revisit React + Tailwind basics to support UI fixes in the MERN stack portal.",
                "duration_weeks": 2,
                "resources": ["JobsUPI React snippets", "Vite/Tailwind crash course"],
            },
            {
                "title": "API ticket drills",
                "description": "Shadow senior devs to triage Express/Mongo API bugs and log AI-agent issues.",
                "duration_weeks": 2,
                "resources": ["Postman collections", "GitHub issue templates"],
            },
        ],
    },
    {
        "role_id": "ai-data-ops-associate",
        "title": "AI Data Ops Associate",
        "skills": {"must_have": {"excel": 1, "python": 1}, "nice_to_have": {"langchain": 1}},
        "personality": ["analytical", "process-driven"],
        "environment": {"mobility": "medium"},
        "roadmap": [
            {
                "title": "Labeling playbook",
                "description": "Learn annotation SOPs for Gemini/LangGraph training data.",
                "duration_weeks": 2,
                "resources": ["Label Studio basics", "QA checklist"],
            },
            {
                "title": "Ops automations",
                "description": "Practice writing Python notebooks that push clean data into Mongo/Redis caches.",
                "duration_weeks": 3,
                "resources": ["FastAPI ops guide", "LangChain tooling demos"],
            },
        ],
    },
    {
        "role_id": "edge-ai-field-tech",
        "title": "Edge AI Field Technician",
        "skills": {"must_have": {"networking": 1}, "nice_to_have": {"iot": 1}},
        "personality": ["hands-on", "problem-solver"],
        "environment": {"mobility": "high"},
        "roadmap": [
            {
                "title": "Device commissioning",
                "description": "Shadow senior techs to deploy IoT sensors that sync with MERN dashboards.",
                "duration_weeks": 3,
                "resources": ["Hardware checklists", "Edge deployment SOP"],
            },
            {
                "title": "AI health checks",
                "description": "Use LangSmith traces and FastAPI probes to validate on-site models.",
                "duration_weeks": 2,
                "resources": ["LangGraph observability guide"],
            },
        ],
    },
]


def _append_error(state: SeekerGraphState, message: str) -> None:
    state.setdefault("errors", []).append(message)


def _extract_text(message: AIMessage) -> str:
    content = message.content
    if isinstance(content, list):
        return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
    return str(content)


def _role_catalog_snapshot(limit: int = 5) -> List[Dict]:
    return [
        {
            "role_id": role["role_id"],
            "title": role["title"],
            "skills": list(role["skills"]["must_have"].keys()),
            "personality": role.get("personality", []),
            "mobility": role.get("environment", {}).get("mobility"),
        }
        for role in ROLE_LIBRARY[:limit]
    ]


@traceable(name="recommend_roles")
def _call_llm_for_recommendations(profile: dict) -> List[RoleRecommendation]:
    llm = get_llm()
    prompt = (
        "You are a job mentor for blue/grey collar workers in India.\n"
        "Given the candidate profile and a role catalog, rank the best 3 roles.\n"
        "Respond ONLY with JSON array items of the form "
        '{"role_id": "...", "title": "...", "match_score": 0.0-1.0, "rationale": "..."}.\n'
        "Do not include any extra text before or after the JSON."
    )
    payload = {
        "profile": profile,
        "catalog": _role_catalog_snapshot(),
    }
    message = llm.invoke(f"{prompt}\nData:\n{json.dumps(payload, ensure_ascii=False)}")
    text = _extract_text(message).strip()
    logger.info("Raw Gemini recommendation output: {}", text)
    start = text.find("[")
    end = text.rfind("]") + 1
    if start == -1 or end == 0:
        raise ValueError("LLM response missing JSON array")
    data = json.loads(text[start:end])
    recommendations: List[RoleRecommendation] = []
    for item in data:
        recommendations.append(
            RoleRecommendation(
                role_id=item["role_id"],
                title=item["title"],
                match_score=float(item["match_score"]),
                rationale=item.get("rationale", "LLM generated rationale"),
            )
        )
    return recommendations


@traceable(name="summarize_recommendation")
def _call_llm_for_summary(role: RoleRecommendation, roadmap: List[RoadmapStep]) -> str:
    llm = get_llm()
    prompt = (
        "Summarize the recommended role and roadmap for an Indian job seeker in one concise paragraph.\n"
        "Highlight why the role fits and how long the roadmap takes.\n"
        "Return plain text response."
    )
    payload = {
        "role": role,
        "roadmap": roadmap,
    }
    message = llm.invoke(f"{prompt}\nData:\n{json.dumps(payload, ensure_ascii=False)}")
    return _extract_text(message).strip()


def _heuristic_recommendations(normalized: dict) -> List[RoleRecommendation]:
    skills = set(normalized.get("skills", []))
    personality = set(normalized.get("personality", []))
    preferred_mobility = normalized.get("preferred_mobility", "medium")

    recommendations: List[RoleRecommendation] = []
    for role in ROLE_LIBRARY:
        role_skills = set(role["skills"]["must_have"].keys()) | set(role["skills"].get("nice_to_have", {}).keys())
        skill_overlap = len(skills & role_skills)
        personality_overlap = len(personality & set(role.get("personality", [])))
        mobility_penalty = 0 if role.get("environment", {}).get("mobility") == preferred_mobility else 1

        score = max(0.1, (skill_overlap * 0.6 + personality_overlap * 0.3) - mobility_penalty * 0.2)
        rationale = (
            "Suggested as a MERN + AI support role that builds on {} skills while exposing you to LangGraph ops."
        ).format(
            ", ".join(sorted(skills)) or "foundational"
        )
        recommendations.append(
            RoleRecommendation(
                role_id=role["role_id"],
                title=role["title"],
                match_score=round(min(score, 1.0), 2),
                rationale=rationale,
            )
        )
    recommendations.sort(key=lambda r: r["match_score"], reverse=True)
    return recommendations[:3]


def collect_profile_node(state: SeekerGraphState) -> SeekerGraphState:
    """Normalize user-provided profile answers into structured attributes."""

    try:
        profile = state.get("seeker_profile") or {}
        if not profile:
            _append_error(state, "Profile inputs missing; defaults applied")
        normalized_profile = {
            "skills": sorted(set(map(str.lower, profile.get("skills", [])))),
            "interests": sorted(set(map(str.lower, profile.get("interests", [])))),
            "personality": sorted(set(map(str.lower, profile.get("personality", [])))),
            "constraints": profile.get("constraints", {}),
            "experience_years": profile.get("experience_years", 0),
            "preferred_mobility": profile.get("preferred_mobility", "medium"),
        }
        logger.debug("Normalized profile: {}", normalized_profile)
        return {**state, "normalized_profile": normalized_profile}
    except Exception as exc:  # pragma: no cover - defensive path
        logger.exception("Profile normalization failed: {}", exc)
        _append_error(state, "Unable to parse seeker profile")
        return state


def role_scoring_node(state: SeekerGraphState) -> SeekerGraphState:
    """Generate deterministic role suggestions using simple heuristic scoring."""

    normalized = state.get("normalized_profile")
    if not normalized:
        _append_error(state, "Profile data missing; cannot score roles")
        return state

    try:
        recommendations = _call_llm_for_recommendations(normalized)
    except Exception as exc:
        logger.exception("Gemini role scoring failed: {}", exc)
        _append_error(state, "Gemini scoring failed; fallback heuristic used")
        recommendations = _heuristic_recommendations(normalized)

    selected_role_id = recommendations[0]["role_id"] if recommendations else None
    return {
        **state,
        "role_candidates": recommendations,
        "selected_role_id": selected_role_id,
    }


def roadmap_builder_node(state: SeekerGraphState) -> SeekerGraphState:
    """Construct a lightweight roadmap for the top-ranked role."""

    selected_role_id = state.get("selected_role_id")
    if not selected_role_id:
        _append_error(state, "No role selected; roadmap generation skipped")
        return state

    role = next((r for r in ROLE_LIBRARY if r["role_id"] == selected_role_id), None)
    if not role:
        _append_error(state, "Selected role not found in library")
        return state

    roadmap_steps: List[RoadmapStep] = role.get("roadmap", [])
    logger.debug("Roadmap for {}: {}", selected_role_id, roadmap_steps)

    return {
        **state,
        "roadmap": roadmap_steps,
    }


def summary_node(state: SeekerGraphState) -> SeekerGraphState:
    """Produce a concise textual summary for downstream channels/UI."""

    role = next((r for r in (state.get("role_candidates") or []) if r["role_id"] == state.get("selected_role_id")), None)
    if not role:
        _append_error(state, "Unable to build summary; missing role context")
        return state

    roadmap = state.get("roadmap", [])
    try:
        summary = _call_llm_for_summary(role, roadmap)
    except Exception as exc:
        logger.exception("Gemini summary generation failed: {}", exc)
        _append_error(state, "Gemini summary failed; fallback used")
        summary = (
            f"Recommended role: {role['title']} (match score {role['match_score']}). "
            f"Estimated roadmap length: {sum(step.get('duration_weeks', 0) for step in roadmap)} weeks."
        )
    logger.debug("Summary generated: {}", summary)
    return {**state, "summary": summary}
