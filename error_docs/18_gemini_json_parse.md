# Gemini JSON Parse Failure

## When it happened
- Date/time: 2025-11-19 ~15:57 IST
- Endpoint: `POST /agents/role-fit`
- Env: Gemini model `gemini-2.5-flash`, LangSmith tracing enabled.

## Symptoms
- API response falls back to heuristic candidates with error `"Gemini scoring failed; fallback heuristic used"`.
- Logs show `Raw Gemini recommendation output:` with blank content followed by `ValueError: LLM response missing JSON array`.
- LangSmith log also warns `LangSmithMissingAPIKeyWarning` before fallback triggers.

## Immediate impact
- Role recommendations rely on heuristic fallback; Gemini output not used.
- No LangSmith trace recorded for the run because API key was missing.

## Notes for fix
- Confirm Gemini key active; log `message.response_metadata` to inspect errors.
- Harden parser to detect structured error payloads.
- Export a valid `LANGSMITH_API_KEY` before starting `uvicorn` so tracing succeeds.
