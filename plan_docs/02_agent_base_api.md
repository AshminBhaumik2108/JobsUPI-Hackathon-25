# Step 2: Agent Service Base API

## Goals
- Scaffold FastAPI application with health routes, configuration management, and logging before integrating LangGraph.
- Catch environment/config issues (from `01_dependency_conflicts.md`, `02_python_version_incompatibility.md`).

## Tasks
1. Create FastAPI entry (`app/main.py`) mounting routers and middleware.
2. Implement `config.py` using `pydantic-settings` for env loading; include validation for Gemini keys, LangSmith keys, Gmail secrets.
3. Add health-check endpoint `/health` plus readiness endpoint verifying dependent services (Redis, Mongo if used).
4. Configure structured logging (Loguru) and exception handlers.
5. Add basic rate limiting middleware (SlowAPI) with in-memory store to prevent abuse.

## Verification Checklist
- `pytest` (or `uvicorn app.main:app --reload`) boots without errors.
- `GET /health` returns 200 in local tests (curl/Postman/httpx).
- Log statements appear with contextual metadata when hitting endpoints.
- Missing env vars raise validation errors instead of silent failures.
