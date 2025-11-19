# Step 6: Core Service Routes

## Goals
- Implement REST APIs in Express to manage auth, seeker profiles, roles, roadmaps, and job searches.
- Ensure endpoints align with contracts consumed by agent service and frontend.

## Tasks
1. Build authentication routes (signup/login) with JWT + bcrypt hashing.
2. CRUD routes:
   - `/profiles`
   - `/roles`
   - `/roadmaps`
   - `/jobs`
3. Query filters for jobs (location, salary, role) and roadmaps (role ID).
4. Middleware: validation (zod/joi), error handler, rate-limiter, request logging.
5. Optionally expose webhook/utility endpoints for syncing data to the agent service.

## Verification Checklist
- Postman/Supertest suite covers success/error cases for each route.
- JWT middleware rejects invalid tokens; protected endpoints tested.
- Responses match schemas defined in `docs/api-contracts.md`.
- Load test (e.g., autocannon) shows acceptable latency under modest traffic.
