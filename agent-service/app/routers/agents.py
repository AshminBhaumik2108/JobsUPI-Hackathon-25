"""FastAPI endpoints for interacting with the LangGraph-powered agents."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from app.schemas.agents import (
    ProfileRequest,
    ProfileResponse,
    RoadmapRequest,
    RoadmapResponse,
    RoleFitRequest,
    RoleFitResponse,
)
from app.services.gmail import send_roadmap_email
from app.services.graph_runner import GraphRunner, get_graph_runner

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/profile", response_model=ProfileResponse)
async def build_profile(
    payload: ProfileRequest,
    runner: GraphRunner = Depends(get_graph_runner),
) -> ProfileResponse:
    """Return normalized profile data based on conversational inputs."""
    state = runner.run({"seeker_profile": payload.seeker_profile.model_dump()})
    if "normalized_profile" not in state:
        logger.error("Normalized profile missing from graph state")
        raise HTTPException(status_code=500, detail="Graph did not return normalized profile")

    return ProfileResponse(
        normalized_profile=state["normalized_profile"],
        errors=state.get("errors", []),
    )


@router.post("/role-fit", response_model=RoleFitResponse)
async def get_role_fit(
    payload: RoleFitRequest,
    runner: GraphRunner = Depends(get_graph_runner),
) -> RoleFitResponse:
    """Run the full pipeline to retrieve role matches and summary."""
    state = runner.run({"seeker_profile": payload.seeker_profile.model_dump()})

    return RoleFitResponse(
        role_candidates=state.get("role_candidates", []),
        selected_role_id=state.get("selected_role_id"),
        summary=state.get("summary"),
        errors=state.get("errors", []),
    )


@router.post("/roadmap", response_model=RoadmapResponse)
async def get_roadmap(
    payload: RoadmapRequest,
    runner: GraphRunner = Depends(get_graph_runner),
) -> RoadmapResponse:
    """Return roadmap for a supplied role or latest recommendation."""
    base_state = {}
    if payload.seeker_profile:
        base_state["seeker_profile"] = payload.seeker_profile.model_dump()
    if payload.role_id:
        base_state["selected_role_id"] = payload.role_id

    state = runner.run(base_state)
    email_status = None
    if payload.email and state.get("summary"):
        email_status = send_roadmap_email(payload.email, state["summary"])

    return RoadmapResponse(
        role_id=state.get("selected_role_id"),
        roadmap=state.get("roadmap", []),
        summary=state.get("summary"),
        email_status=email_status,
        errors=state.get("errors", []),
    )
