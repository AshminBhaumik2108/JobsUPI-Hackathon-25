# Problem: LangGraph Node Name Conflicts with State Key

## Context
After adding the `/agents/graph-preview` endpoint, the server began throwing an exception whenever that endpoint was invoked. Other endpoints worked fine. The stack trace referenced `langgraph/graph/state.py`.

## Error Message
```
ValueError: 'delivery' is already being used as a state key
```

## Root Cause
Inside `graph/notification_graph.py`, we declared a state dictionary with a key named `delivery`, and we also added a node to the graph named `"delivery"`. LangGraph uses node names as state keys by default. When both the node name and an existing key collide, the graph builder raises this error to prevent ambiguous state updates.

## Step-by-Step Solution
1. **Rename the node identifier:**
   - Open `graph/notification_graph.py`.
   - Change the node name to something unique, e.g. `delivery_step`:
     ```python
     graph.add_node("delivery_step", run_delivery)
     graph.add_edge("channels", "delivery_step")
     graph.add_edge("delivery_step", "tracking")
     ```
   - Keep the state key as `state["delivery"]` inside `run_delivery`; only the node label needs to change.

2. **Reload the server:**
   ```bash
   uvicorn api.main:app --reload
   ```

3. **Test the graph endpoint:**
   ```bash
   curl "http://localhost:8000/agents/graph-preview?limit=4"
   ```
   The response should now succeed.

## Prevention Tips
- When building LangGraph workflows, ensure node names differ from keys stored in the state dictionary.
- Adopt a naming convention (`*_step`, `node_*`, etc.) to make collisions less likely.
- Review the graph diagram (ASCII or Mermaid) to spot duplicate names early.

## Validation Steps
- Call `/agents/graph-preview` and confirm it returns structured data instead of a traceback.
- Compare output with `/agents/notification-preview` to ensure the logic still aligns.
