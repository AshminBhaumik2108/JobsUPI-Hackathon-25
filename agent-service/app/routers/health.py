from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Basic health check")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/readiness", summary="Readiness check")
async def readiness() -> dict[str, str]:
    # TODO: add checks for Redis, Mongo, etc. when integrated
    return {"status": "ready"}
