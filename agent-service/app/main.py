"""Application entrypoint for the JobsUPI Agent Service."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.middleware.rate_limit import init_rate_limiter, limiter
from app.middleware.request_context import RequestContextMiddleware
from app.routers import api_router
from app.routers import agents as agents_router

settings = get_settings()

app = FastAPI(
    title="JobsUPI Agent Service",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(settings.app_base_url).rstrip("/")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestContextMiddleware, log_level=settings.log_level)

init_rate_limiter(app)
register_exception_handlers(app)

app.state.settings = settings

app.include_router(api_router)
app.include_router(agents_router.router)


@app.get("/", tags=["root"])
@limiter.limit(settings.rate_limit_default)
async def root(request: Request) -> dict[str, str]:
    """Simple endpoint for quick verifications and smoke tests."""
    logger.bind(request_id=request.headers.get("X-Request-ID", "-")).info(
        "Root endpoint invoked from {}", request.client.host if request.client else "unknown"
    )
    return {"message": "JobsUPI agent service is running"}
