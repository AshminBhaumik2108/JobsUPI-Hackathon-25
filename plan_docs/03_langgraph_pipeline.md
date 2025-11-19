# Step 3: LangGraph Pipeline Construction

## Goals
- Build conversation state machine for seeker intake, role fit, and roadmap generation using LangGraph + LangChain.
- Prevent graph configuration issues highlighted in `05_langgraph_compiledgraph_import.md`, `06_langgraph_node_name_conflict.md`, `07_langgraph_missing_state_key.md`, and `17_langgraph_channel_decisions_lost_in_state.md`.

## Tasks
1. Define state schema (skills, interests, constraints, conversation history, role shortlist, roadmap summary).
2. Implement nodes:
   - `collect_profile_node`
   - `role_scoring_node`
   - `roadmap_builder_node`
   - `summary_node`
3. Assemble graph with explicit channels, names, and transitions; include guardrails for missing data.
4. Configure LangChain tools (Gemini model wrappers, retrieval over role templates, fallback models).
5. Register tracing via LangSmith for each run; add deterministic mock runner for tests.

## Verification Checklist
- `langgraph graph inspect` (or similar) succeeds; no missing keys/conflicts.
- Unit tests mock LLM responses and assert state transitions.
- Sample graph run (script) produces deterministic JSON for fixture input.
- LangSmith trace appears complete and labeled per run ID.
