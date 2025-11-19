# Step 10: Integration & Regression Testing

## Goals
- Validate full workflow with both servers and frontend communicating over their respective ports.
- Catch regressions early by automating sanity checks.

## Tasks
1. Spin up Mongo, core service, agent service, and frontend locally (Docker or separate terminals).
2. Run scripted E2E scenario:
   - Start from empty profile, complete conversation, receive roles, choose one, view roadmap, browse jobs, trigger email.
3. Capture logs from both backends; ensure correlation IDs span requests.
4. Execute automated E2E tests (Playwright/Cypress) covering core journey.
5. Perform lightweight load test on key endpoints (`/agents/role-fit`, `/jobs`).

## Verification Checklist
- Manual walkthrough completes with expected data displayed and no 4xx/5xx errors.
- Automated E2E tests pass in CI (headless browsers) with seeded data.
- Load test shows stable latency and no memory leaks.
- Recorded demo video taken during a successful run.
