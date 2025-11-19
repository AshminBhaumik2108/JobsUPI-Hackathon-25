"""Utility helpers for initializing Gemini LLM clients."""

from __future__ import annotations

from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI
from loguru import logger

from app.config import get_settings


@lru_cache
def get_llm() -> ChatGoogleGenerativeAI:
    """Return a cached Gemini chat client configured from environment variables."""

    settings = get_settings()
    try:
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model_name,
            google_api_key=settings.google_api_key,
            temperature=0.2,
            max_output_tokens=1024,
        )
    except Exception as exc:  # pragma: no cover - initialization failure
        logger.exception("Failed to initialize Gemini client: {}", exc)
        raise
