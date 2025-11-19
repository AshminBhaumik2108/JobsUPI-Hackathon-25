"""Pydantic request/response schemas for agent endpoints."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ConstraintModel(BaseModel):
    location: Optional[str] = None
    salary_expectation: Optional[int] = Field(default=None, ge=0)
    availability: Optional[str] = None


class SeekerProfilePayload(BaseModel):
    skills: List[str] = []
    interests: List[str] = []
    personality: List[str] = []
    constraints: ConstraintModel = ConstraintModel()
    experience_years: int = Field(default=0, ge=0)
    preferred_mobility: Optional[str] = "medium"


class ProfileRequest(BaseModel):
    seeker_profile: SeekerProfilePayload


class ProfileResponse(BaseModel):
    normalized_profile: dict
    errors: List[str] = []


class RoleFitRequest(BaseModel):
    seeker_profile: SeekerProfilePayload


class RoleRecommendationModel(BaseModel):
    role_id: str
    title: str
    match_score: float
    rationale: str


class RoleFitResponse(BaseModel):
    role_candidates: List[RoleRecommendationModel]
    selected_role_id: Optional[str]
    summary: Optional[str]
    errors: List[str] = []


class RoadmapRequest(BaseModel):
    seeker_profile: Optional[SeekerProfilePayload] = None
    role_id: Optional[str] = None
    email: Optional[str] = None


class RoadmapStepModel(BaseModel):
    title: str
    description: str
    duration_weeks: Optional[int] = None
    resources: List[str] = []


class RoadmapResponse(BaseModel):
    role_id: Optional[str]
    roadmap: List[RoadmapStepModel]
    summary: Optional[str]
    email_status: Optional[str]
    errors: List[str] = []
