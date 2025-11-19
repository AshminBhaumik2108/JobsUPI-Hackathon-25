"""Health and readiness endpoints for infrastructure monitoring."""

from fastapi import APIRouter
from loguru import logger

router = APIRouter()


@router.get("/health", summary="Basic health check")
async def health() -> dict[str, str]:
    """Return liveness information for basic smoke tests."""
    logger.bind(request_id="-").debug("Health check invoked")
    return {"status": "ok"}


@router.get("/readiness", summary="Readiness check")
async def readiness() -> dict[str, str]:
    """Return readiness status (expand with downstream checks when available)."""
    logger.bind(request_id="-").debug("Readiness check invoked")
    # TODO: add checks for Redis, Mongo, etc. when integrated
    return {"status": "ready"}
