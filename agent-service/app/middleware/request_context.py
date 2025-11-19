"""Middleware that attaches a correlation ID and configures logging per request."""

import uuid
from typing import Callable

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import configure_logging, get_request_id, set_request_id


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Injects request IDs and ensures incoming calls are logged consistently."""

    def __init__(self, app, log_level: str = "INFO"):
        super().__init__(app)
        configure_logging(log_level)

    async def dispatch(self, request: Request, call_next: Callable):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        set_request_id(request_id)
        logger.bind(request_id=request_id).info(
            "Incoming request {} {}", request.method, request.url.path
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            logger.bind(request_id=request_id).exception(
                "Unhandled error while processing {} {}: {}", request.method, request.url.path, exc
            )
            raise

        response.headers["X-Request-ID"] = get_request_id() or "-"
        logger.bind(request_id=request_id).info(
            "Outgoing response {} {} -> {}", request.method, request.url.path, response.status_code
        )
        return response
