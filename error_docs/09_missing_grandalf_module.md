# Problem: Missing `grandalf` Module for Graph Visualisation

## Context
To render the LangGraph workflow as an ASCII or Mermaid diagram, we ran a helper script that called `compiled.get_graph().draw_ascii()`. The script crashed with an import error originating from LangChain’s graph visualisation utilities.

## Error Message
```
ModuleNotFoundError: No module named 'grandalf'
```

## Root Cause
The `draw_ascii()` helper relies on the optional `grandalf` library to compute graph layouts (Sugiyama algorithm). This package is not installed automatically with LangGraph or LangChain. Without it, the visualisation code cannot determine how to position nodes.

## Step-by-Step Solution
1. **Install `grandalf` inside the virtual environment:**
   ```bash
   source .venv/bin/activate
   pip install grandalf
   ```
2. **Re-run the visualisation script:**
   ```bash
   python graph-view.txt  # or the inline script provided in the README
   ```
   The ASCII diagram should now print successfully.

## Prevention Tips
- Treat `grandalf` as an optional developer dependency; consider adding it to `requirements-dev.txt` if you create one.
- Mention the requirement in documentation so team members know to install it before rendering graphs.
- If you share notebooks or scripts that draw graphs, include a quick import guard:
  ```python
  try:
      import grandalf
  except ImportError:
      raise RuntimeError("Install grandalf to view LangGraph diagrams: pip install grandalf")
  ```

## Validation Steps
- Run the ASCII visualisation command again and confirm it prints the node/edge structure.
- Optionally generate a Mermaid file (`draw_mermaid("notification_graph.mmd")`) and preview it in a Markdown viewer.
