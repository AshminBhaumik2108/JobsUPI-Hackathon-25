# Step 8: Frontend Setup

## Goals
- Bootstrap Vite + React + TypeScript app with Tailwind (or Chakra) and shared context/state utilities.
- Ensure API clients and environment configs are ready before feature work.

## Tasks
1. Initialize Vite project (`client/`), install React Query, Tailwind, router.
2. Configure `tailwind.config.js`, `postcss.config.js`, and base styles.
3. Create global context provider (useContext) for seeker profile + UI state; no Redux/Zustand.
4. Build API clients (`agentClient`, `coreClient`) using Axios/fetch with base URLs from env.
5. Add routing skeleton (profile, roles, roadmap, jobs, dashboard pages) with lazy loading.

## Verification Checklist
- `npm run dev` starts successfully; Tailwind styles applied to placeholder components.
- Context provider supplies default state; test components read/write without errors.
- API clients hit mock servers; environment switching works.
- ESLint/TypeScript build passes.
