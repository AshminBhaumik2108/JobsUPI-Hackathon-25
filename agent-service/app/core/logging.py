"""Utilities for configuring Loguru logging and per-request correlation IDs."""

from contextvars import ContextVar
from typing import Any

from loguru import logger

_request_id_ctx_var: ContextVar[str | None] = ContextVar("request_id", default=None)


def set_request_id(request_id: str | None) -> None:
    """Attach the provided request ID to the current async context."""
    _request_id_ctx_var.set(request_id)


def get_request_id() -> str | None:
    """Return the request ID associated with the current async context."""
    return _request_id_ctx_var.get()


def configure_logging(level: str = "INFO") -> None:
    """Configure Loguru with a consistent format and desired log level."""
    logger.remove()
    # Ensure a default request_id is always present to avoid KeyError in formatters.
    logger.configure(extra={"request_id": "-"})
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=level.upper(),
        backtrace=False,
        diagnose=False,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[request_id]} | {message}",
    )


class RequestIDFilter:
    """Helper that can be used when extra request ID propagation is required."""

    def __init__(self) -> None:
        self._token: ContextVar[Any] | None = None

    def __call__(self, request_id: str | None) -> None:
        set_request_id(request_id)


def log_message(message: str) -> None:
    """Log an informational message with the bound request ID, if present."""
    logger.bind(request_id=get_request_id() or "-").info(message)
