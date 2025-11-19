"""Helper for simulating roadmap emails via Gmail credentials."""

from __future__ import annotations

from loguru import logger

from app.config import get_settings


def send_roadmap_email(recipient: str, summary: str) -> str:
    """Simulate sending the roadmap email. Returns status message."""

    settings = get_settings()
    if not all([settings.gmail_client_id, settings.gmail_client_secret, settings.gmail_refresh_token]):
        warning = "Gmail credentials missing; email skipped"
        logger.warning(warning)
        return warning

    logger.info("(Simulated) sending roadmap summary to {}", recipient)
    return "queued"
