"""Centralized configuration and model factory for Google ADK agents."""

from __future__ import annotations

import os
from dotenv import load_dotenv
from google.adk.models.google_llm import Gemini
from google.genai import types

load_dotenv()

# Default Gemini model requested for the workshop patterns
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


def get_retry_config(
    attempts: int = 5,
    exp_base: float = 7.0,
    initial_delay: float = 1.0,
    http_status_codes: list[int] | None = None,
) -> types.HttpRetryOptions:
    """Creates a resilient HTTP retry configuration for LLM requests.

    Args:
        attempts: Maximum retry attempts.
        exp_base: Exponential backoff delay multiplier.
        initial_delay: Initial delay in seconds.
        http_status_codes: HTTP status codes to retry on.

    Returns:
        Configured HttpRetryOptions instance.
    """
    return types.HttpRetryOptions(
        attempts=attempts,
        exp_base=exp_base,
        initial_delay=initial_delay,
        http_status_codes=http_status_codes or [429, 500, 503, 504],
    )


def get_model(
    model_name: str | None = None,
    retry_config: types.HttpRetryOptions | None = None,
) -> Gemini:
    """Instantiates a Gemini model wrapper configured with retry policies.

    Args:
        model_name: Target model identifier (defaults to GEMINI_MODEL or gemini-3.5-flash).
        retry_config: Optional custom HttpRetryOptions.

    Returns:
        Configured Gemini model instance.
    """
    resolved_model = model_name or DEFAULT_MODEL
    resolved_retry = retry_config or get_retry_config()
    return Gemini(model=resolved_model, retry_options=resolved_retry)
