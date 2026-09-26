"""Unit tests for centralized common utilities (config, runner)."""

import os
import pytest
from google.adk.agents import Agent
from patterns.agents.common.config import DEFAULT_MODEL, get_model, get_retry_config
from patterns.agents.common.runner import get_runner


def test_default_model_configuration():
    """Verify that DEFAULT_MODEL defaults to gemini-3.5-flash unless overridden."""
    expected_default = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    assert DEFAULT_MODEL == expected_default


def test_get_retry_config():
    """Verify retry options construction and defaults."""
    retry = get_retry_config(attempts=3, exp_base=2.0)
    assert retry.attempts == 3
    assert retry.exp_base == 2.0
    assert 429 in retry.http_status_codes
    assert 500 in retry.http_status_codes


def test_get_model():
    """Verify Gemini model wrapper initialization."""
    model = get_model()
    assert model.model == os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

    custom_model = get_model("gemini-custom-model")
    assert custom_model.model == "gemini-custom-model"


@pytest.mark.asyncio
async def test_get_runner():
    """Verify ADK Runner and InMemorySessionService creation."""
    dummy_agent = Agent(name="test_dummy_agent")
    runner, user_id, session_id = await get_runner(
        root_agent=dummy_agent,
        app_name="test_app",
        user_id="test_user",
        session_id="test_session_123",
    )

    assert runner.agent.name == "test_dummy_agent"
    assert user_id == "test_user"
    assert session_id == "test_session_123"
    assert runner.app_name == "test_app"
