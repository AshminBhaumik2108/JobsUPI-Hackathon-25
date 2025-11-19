"""Helpers for configuring API rate limiting with SlowAPI."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config import get_settings

limiter = Limiter(key_func=get_remote_address)


def init_rate_limiter(app: FastAPI) -> None:
    """Attach rate limiting and an exception handler to the provided FastAPI app."""
    settings = get_settings()

    app.state.rate_limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):  # type: ignore
        limit_value = getattr(exc, "limit", settings.rate_limit_default)
        logger.bind(request_id=request.headers.get("X-Request-ID", "-")).warning(
            "Rate limit exceeded for {} {} (limit={})", request.method, request.url.path, limit_value
        )
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Too many requests",
                "limit": limit_value,
            },
        )

    app.state.rate_limit_default = settings.rate_limit_default
