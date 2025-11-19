# Step 1: Environment & Repo Skeleton

## Goals

- Establish shared repository structure and base configs before writing feature code.
- Ensure Python and Node environments match required versions to avoid compatibility issues noted in `error_docs`.

## Tasks

1. Create root folders: `agent-service/`, `core-service/`, `client/`, `docs/`, `error_docs/`, `plan_docs/`.
2. Initialize git repo (if not already) and commit baseline structure.
3. Python setup:
   - Choose supported Python version (>=3.10 per FastAPI/LangChain requirements).
   - Create virtual environment, install FastAPI dependencies.
   - Add `requirements.txt`/`pyproject.toml` plus `.env.example` with placeholder keys.
4. Node setup for core-service:
   - Initialize `package.json`, install Express/Mongoose tooling, add `.env.example`.
5. Global scripts folder with helper start scripts (optional but recommended).

## Verification Checklist

- `python --version` matches documented version, `pip list` shows correct packages.
- `npm run lint` / `npm run test` placeholders execute without errors in both services.
- `.env.example` files exist and include required variables for Mongo URI, Gemini API key, Gmail creds, etc.
- Git status clean after initial commit.
