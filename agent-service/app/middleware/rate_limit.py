from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config import get_settings

limiter = Limiter(key_func=get_remote_address)


def init_rate_limiter(app: FastAPI) -> None:
    settings = get_settings()

    app.state.rate_limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(_: Request, exc: RateLimitExceeded):  # type: ignore
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Too many requests",
                "limit": getattr(exc, "limit", settings.rate_limit_default),
            },
        )

    app.state.rate_limit_default = settings.rate_limit_default
