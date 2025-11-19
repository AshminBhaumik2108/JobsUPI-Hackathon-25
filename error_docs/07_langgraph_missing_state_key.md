# Problem: `KeyError` for `channel_decisions` in LangGraph

## Context
Shortly after fixing the node naming issue, hitting `/agents/graph-preview` produced a new error. This time the stack trace pointed to `run_delivery` in our LangGraph workflow.

## Error Message
```
KeyError: 'channel_decisions'
```

## Root Cause
In certain runs (for example, when no messages pass the sender filter), the `channels` node may not set `state["channel_decisions"]` before the delivery node executes. Our original code accessed `state["channel_decisions"]` directly, which crashes if the key is missing.

## Step-by-Step Solution
1. **Guard the dictionary access:**
   - Open `graph/notification_graph.py`.
   - Update `run_delivery` so it uses a default when the key is absent:
     ```python
     def run_delivery(state: NotificationState) -> NotificationState:
         channel_decisions = state.get("channel_decisions", [])
         delivery = delivery_agent.run(state["notifications"], channel_decisions)
         state["delivery"] = delivery
         return state
     ```

2. **Restart the server:**
   ```bash
   uvicorn api.main:app --reload
   ```

3. **Try the graph endpoint again:**
   ```bash
   curl "http://localhost:8000/agents/graph-preview?limit=4"
   ```
   The endpoint now returns data even when no channels are chosen.

## Prevention Tips
- When passing state between LangGraph nodes, treat the state dictionary as untrusted input—always use `.get()` or `dict.setdefault` for optional fields.
- Consider initialising default values in the state payload before invoking the graph.
- Write short unit tests (or manual checks) covering edge cases such as “zero messages”, “all filtered out”, etc.

## Validation Steps
- Execute `/agents/graph-preview` with `limit=1` and an impossible query (e.g. `query=from:nothing@example.com`). The response should succeed with zero counts, not a stack trace.
- Double-check that the normal happy path still produces notifications and channel rationales.
