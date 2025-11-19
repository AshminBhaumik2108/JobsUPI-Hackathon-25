"""Custom exception handlers with structured logging."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger


def register_exception_handlers(app: FastAPI) -> None:
    """Register FastAPI exception handlers that emit structured logs."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError):  # type: ignore
        logger.bind(request_id="-").warning("Validation error: {}", exc.errors())
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(_: Request, exc: Exception):  # type: ignore
        logger.bind(request_id="-").exception("Unhandled server error: {}", exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "message": str(exc)},
        )
