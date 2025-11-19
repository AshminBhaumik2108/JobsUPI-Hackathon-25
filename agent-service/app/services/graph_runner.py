"""Wrapper utilities for invoking the LangGraph pipeline with logging."""

from __future__ import annotations

from typing import Any, Dict

from loguru import logger
from langsmith import Client
from langsmith.run_trees import RunTree

from app.config import get_settings
from app.graph import build_seeker_graph


class GraphRunner:
    """Encapsulates execution of the seeker LangGraph for reuse across endpoints."""

    def __init__(self) -> None:
        self.graph = build_seeker_graph()
        settings = get_settings()
        self.langsmith_project = settings.langsmith_project or settings.langchain_project
        try:
            api_key = settings.langsmith_api_key or settings.langchain_api_key
            self.langsmith_client = Client(api_key=api_key) if api_key else None
        except Exception as exc:  # pragma: no cover - init failure shouldn't block graph
            logger.warning("LangSmith client initialization failed: {}", exc)
            self.langsmith_client = None

    def run(self, initial_state: Dict[str, Any], request_id: str | None = None) -> Dict[str, Any]:
        """Invoke the LangGraph pipeline and return the resulting state."""

        run_tree: RunTree | None = None
        if self.langsmith_client:
            run_tree = RunTree(
                name="seeker-graph",
                run_type="chain",
                inputs=initial_state,
                project_name=self.langsmith_project,
                metadata={"request_id": request_id} if request_id else None,
            )
        try:
            result = self.graph.invoke(initial_state)
            logger.debug("Graph run completed with keys: {}", list(result.keys()))
            if run_tree and self.langsmith_client:
                run_tree.end(outputs=result)
                run_tree.post(self.langsmith_client)
            return result
        except Exception as exc:  # pragma: no cover - defensive path
            logger.exception("Graph invocation failed: {}", exc)
            if run_tree:
                run_tree.end(outputs={}, error=str(exc))
            raise


def get_graph_runner() -> GraphRunner:
    """Factory returning a GraphRunner instance (cached via FastAPI dependency)."""
    return GraphRunner()
