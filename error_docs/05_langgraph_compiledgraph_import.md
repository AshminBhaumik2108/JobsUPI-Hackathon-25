# Problem: `ImportError` for `CompiledGraph` in LangGraph

## Context
After wiring the LangGraph workflow we restarted the FastAPI server. `uvicorn` crashed immediately with an import error pointing to `graph/notification_graph.py`.

## Error Message
```
ImportError: cannot import name 'CompiledGraph' from 'langgraph.graph'
```

## Root Cause
We tried to import `CompiledGraph` directly from `langgraph.graph`. In LangGraph version `0.2.40`, this symbol is not exported from that module. The library expects you to call `.compile()` on a `StateGraph` return value when you need a compiled instance, without referencing the class at import time.

## Step-by-Step Solution
1. **Edit the graph module:**
   - Open `graph/notification_graph.py`.
   - Remove `CompiledGraph` from the import list:
     ```python
     # from langgraph.graph import END, StateGraph, CompiledGraph  # old
     from langgraph.graph import END, StateGraph  # new
     ```
   - Where we needed typing support, we replaced `CompiledGraph` annotations with `Any` and compiled the graph dynamically inside `invoke_graph` by checking `hasattr(graph, "compile")`.

2. **Restart `uvicorn`:**
   ```bash
   uvicorn api.main:app --reload
   ```

3. **Hit `/agents/graph-preview`:**
   - Confirm the endpoint responds without the import error.

## Prevention Tips
- When in doubt about library exports, check the official documentation or run `dir()` in a Python shell.
- Avoid hard-coding type hints for internal classes unless the library’s version guarantees their presence.
- Use feature detection (`hasattr`) when compiling or invoking graphs so your code handles both compiled and uncompiled objects gracefully.

## Validation Steps
- Restart the server; ensure no import errors appear.
- Test both `/agents/notification-preview` and `/agents/graph-preview`.
- Render the graph (optional) to ensure `build_notification_graph` still works.
