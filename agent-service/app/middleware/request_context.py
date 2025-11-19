import uuid
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import configure_logging, get_request_id, set_request_id


class RequestContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, log_level: str = "INFO"):
        super().__init__(app)
        configure_logging(log_level)

    async def dispatch(self, request: Request, call_next: Callable):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        set_request_id(request_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = get_request_id() or "-"
        return response
