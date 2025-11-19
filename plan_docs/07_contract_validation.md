# Step 7: Cross-Service Contract Validation

## Goals
- Keep agent service, core service, and frontend aligned on payload formats.
- Avoid runtime mismatches by enforcing schemas and running automated checks.

## Tasks
1. Document request/response DTOs in `docs/api-contracts.md` (Pydantic + TypeScript equivalents).
2. Create shared JSON schema or OpenAPI snippets that both services reference.
3. Write contract tests:
   - Agent service mocks core responses.
   - Core service serves sample payloads validated against schema.
4. Add CI script that runs schema validation and fails on breaking changes.
5. Provide sample payload fixtures for frontend integration tests.

## Verification Checklist
- Schema files pass validation tool (e.g., `ajv`, `pydantic` parsing).
- Contract tests run in both services and in CI.
- Any schema change requires updating fixtures; pipeline blocks until aligned.
- Frontend type generation (if using `openapi-typescript`) outputs up-to-date types.
