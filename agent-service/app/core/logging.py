from contextvars import ContextVar
from typing import Any

from loguru import logger

_request_id_ctx_var: ContextVar[str | None] = ContextVar("request_id", default=None)


def set_request_id(request_id: str | None) -> None:
    _request_id_ctx_var.set(request_id)


def get_request_id() -> str | None:
    return _request_id_ctx_var.get()


def configure_logging(level: str = "INFO") -> None:
    logger.remove()
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=level.upper(),
        backtrace=False,
        diagnose=False,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[request_id]} | {message}",
    )


class RequestIDFilter:
    def __init__(self) -> None:
        self._token: ContextVar[Any] | None = None

    def __call__(self, request_id: str | None) -> None:
        set_request_id(request_id)


def log_message(message: str) -> None:
    logger.bind(request_id=get_request_id() or "-").info(message)
