# JobsUPI Hackathon Portal 🚀🇮🇳

## 1. What Is This Application? 🧭
JobsUPI is a multi-service platform that pairs AI guidance with curated data so Indian job seekers can discover roles, build skills, and land jobs quickly. It has three cooperating layers:
- **AI Agent Service (FastAPI + LangGraph)** for conversational guidance.
- **Core Service (Express + MongoDB)** for structured data (profiles, roles, roadmaps, jobs).
- **Client App (Vite + React)** for a low-literacy-friendly UI.

## 2. Purpose 🌱
Many Indian seekers lack tailored guidance. JobsUPI addresses this by:
- Conversational onboarding (text) that adapts to language comfort.
- AI reasoning to map skills, constraints, and aspirations to real roles.
- Guided learning paths and job feeds tied to each role.
- Email-ready summaries for mentors or hiring partners.

Result: faster clarity, actionable next steps, and equitable access.

## 3. How the Pieces Work Together ⚙️
| Layer      | Responsibilities |
|------------|------------------|
| **AI Agents** (`agent-service`) | Collect profile data, score roles via LangGraph nodes, build learning roadmaps, summarize next steps, send simulated emails. |
| **Core Service** (`core-service`) | Stores seeker profiles, role templates, roadmaps, and job postings with MongoDB + Mongoose. Exposes REST routes consumed by both AI agents and frontend. |
| **Client** (`client`) | React UI with React Query + Tailwind; orchestrates the conversational wizard, role selection, roadmap viewer, job explorer, and dashboard.

Data flow: Client calls AI endpoints (FastAPI) for intelligent responses, AI may call Core for structured data, Client also hits Core directly for jobs/roadmaps. Shared schemas keep payloads consistent.

## 4. Agent Types & Rationale 🤖
1. **Profile Intake Agent** – conversationally gathers seeker info, normalizes to structured profile; prevents incomplete data.
2. **Role Fit Agent** – uses LangGraph scoring node to rank roles with rationales; ensures personalized recommendations.
3. **Roadmap Builder Agent** – converts chosen role + profile gaps into milestone steps; keeps learners focused.
4. **Summary/Email Agent** – packages decisions into Gmail-ready summaries (dry-run) so seekers can share plans.

Each agent isolates a conversation phase, making it easier to test, trace, and reuse.

## 5. Connectivity for Smooth Ops 🔗
- Shared environment configs and schema contracts ensure Agent/Core/Client agree on fields.
- Correlation IDs travel via headers so logs from both services can be stitched together.
- Rate limiting, retries, and health checks prevent cascading failures.
- Seed scripts keep Core data aligned with Agent expectations; mock servers enable frontend dev without live AI.

## 6. Tech Stack by Folder 🧰
- `agent-service`: Python 3.10+, FastAPI, LangGraph/LangChain, Pydantic, Loguru, SlowAPI, Gmail helper, Redis (optional for rate limiting).
- `core-service`: Node.js + Express, Mongoose, JWT/bcrypt, Zod/Joi validation, seed scripts, Supertest/Jest.
- `client`: Vite + React + TypeScript, React Router, React Query, TailwindCSS, Axios API clients.

## 7. UI Workflows for Roadmaps/Profile/Roles/Jobs 🖥️
1. **Profile Wizard** – multi-step conversational form, voice/text friendly; stores state via context and hits `POST /agents/profile`.
2. **Role Recommendations View** – cards show ranked roles, rationales, constraints fit; integrates `POST /agents/role-fit`.
3. **Roadmap Timeline** – visual steps per role from `GET /roadmaps/:roleId`; highlights completed vs upcoming tasks.
4. **Jobs Explorer** – filters (location, salary, role) query `GET /jobs`; React Query handles caching, skeletons manage loading.
5. **Dashboard & Email CTA** – recap profile, selected role, progress tracker, simulated Gmail send for accountability.

## 8. Outcome & Impact for India 🇮🇳
- **Outcome:** Seekers exit with a clear role choice, personalized learning roadmap, and live job leads.
- **Impact:** Reduces guidance gap for low-literacy or first-time job seekers, supports upskilling for Bharat’s workforce, and accelerates employment by contextualizing roles to local constraints (location, pay, language).

---

## Design Challenge Response ✅

**Step 1: Build profile through conversational questions**  
- Profile Intake Agent asks simple, multilingual prompts (voice/text), stores normalized data via FastAPI + LangGraph.

**Step 2: Discover fitting roles**  
- Role Fit Agent scores roles using skills, interests, constraints fetched from Core templates, returning ranked cards.

**Step 3: Select role with guidance**  
- Client UI highlights pros/cons per role, suggested salary/location fit, and allows selecting one with confirmation.

**Step 4: Receive learning roadmap**  
- Roadmap Builder Agent maps gaps to steps (courses, apprenticeships). Client timeline visualizes milestones; summaries can be emailed.

**Step 5: View recommended jobs**  
- Core Service exposes filtered `GET /jobs`; Client shows curated listings aligned with chosen role and profile attributes, updating dynamically.

Together, these steps form the JobsUPI portal—a conversational, AI-assisted journey from self-knowledge to actionable employment pathways for Indian job seekers.