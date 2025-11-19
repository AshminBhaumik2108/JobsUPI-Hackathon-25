# Step 4: Agent API Endpoints

## Goals
- Expose FastAPI routes that leverage the LangGraph pipeline safely and consistently.
- Ensure response schemas match frontend contracts and errors are observable.

## Tasks
1. Implement routers:
   - `POST /agents/profile` → runs intake segment, returns normalized seeker profile summary.
   - `POST /agents/role-fit` → runs scoring nodes, returns ranked roles + rationale.
   - `POST /agents/roadmap` → generates personalized learning steps.
2. Apply Pydantic models for request/response validation.
3. Add middleware for authentication (if required), rate limiting, and structured error responses.
4. Integrate Gmail helper (dry-run) for roadmap emailing; handle quota/403 issues (`03_gmail_oauth_403_error.md`, `10_gmail_api_multiple_calls.md`).
5. Instrument logs/metrics; ensure LangSmith trace IDs propagate via headers.

## Verification Checklist
- Postman/HTTPX tests succeed with sample payloads; responses conform to schema.
- Error paths (missing fields, model failure) return descriptive messages and 4xx/5xx codes.
- Gmail helper logs simulated send without crashing when credentials absent.
- Load test (small burst) confirms rate limiting works and no resource leaks.
