"""Typed state definitions shared across LangGraph nodes."""

from __future__ import annotations

from typing import List, Optional, TypedDict


class RoleRecommendation(TypedDict):
    """Represents a single recommended role entry."""

    role_id: str
    title: str
    match_score: float
    rationale: str


class RoadmapStep(TypedDict, total=False):
    """Represents one roadmap milestone in the learning journey."""

    title: str
    description: str
    duration_weeks: int
    resources: List[str]


class SeekerGraphState(TypedDict, total=False):
    """Top-level state passed between LangGraph nodes."""

    seeker_profile: dict
    normalized_profile: dict
    role_candidates: List[RoleRecommendation]
    selected_role_id: Optional[str]
    roadmap: List[RoadmapStep]
    summary: str
    conversation_history: List[str]
    errors: List[str]
