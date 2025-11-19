# Step 5: Core Service Models & Database

## Goals
- Define MongoDB schemas and seed data to support seeker profiles, roles, and jobs.
- Ensure timestamps and data integrity issues (see `16_database_timestamp_previous_date.md`) are resolved early.

## Tasks
1. Configure MongoDB Atlas connection with retry logic, health check, and logging.
2. Create Mongoose models:
   - `UserProfile`
   - `RoleTemplate`
   - `Roadmap`
   - `JobPosting`
3. Seed initial data sets for roles, roadmaps, and jobs to enable demos without external feeds.
4. Implement utility scripts for importing/exporting data (used by agent service if needed).
5. Add indexes for frequent queries (role type, location, salary range).

## Verification Checklist
- `npm run test:models` validates schema hooks and timestamps.
- Seed script runs without duplication; verify data via Mongo shell/Compass.
- Connection errors are surfaced clearly in logs.
- Documents include created/updated timestamps reflecting actual run time.
