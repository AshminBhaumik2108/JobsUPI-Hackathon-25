# Step 9: Frontend Feature Implementation

## Goals
- Build seeker journey screens incrementally, validating each with backend mocks before moving on.
- Keep UX accessible with simple text-first interactions.

## Tasks & Tests
1. **Profile Conversation Page**
   - Implement multi-step form/wizard using simple prompts.
   - Integrate with `POST /agents/profile`.
   - Tests: component unit tests, mock API success/error states, ensure inputs save to context.
2. **Role Recommendations View**
   - Display ranked roles with rationales, allow selection.
   - Integrate `POST /agents/role-fit`.
   - Tests: verify cards render sorted, selection updates context, handles empty results.
3. **Roadmap Timeline**
   - Timeline/steps UI pulling from `GET /roadmaps/:roleId` (core service).
   - Tests: timeline renders milestones; fallback copy for missing data.
4. **Job Listings & Filters**
   - Fetch from `GET /jobs` with query params.
   - Tests: filter interactions, loading skeletons, error messaging.
5. **Dashboard & Email CTA**
   - Recap profile, chosen role, progress tracker, Gmail send action.
   - Tests: CTA triggers backend call, displays confirmation/toasts.
6. **Global Polish**
   - Accessibility pass, responsive layout, skeleton/loading states, error boundaries.

## Verification Checklist
- Manual E2E flow using mock servers completes without console errors.
- React Query cache updates per navigation; context resets properly on logout/new user.
- Lighthouse/accessibility check passes basic thresholds.
