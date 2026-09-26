"""Mock execution tests for call_agent_async without external API calls."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from google.genai import types
from patterns.agents.common.runner import call_agent_async


class MockEvent:
    def __init__(self, is_final: bool, text: str | None = None, escalate: bool = False, err: str | None = None):
        self._is_final = is_final
        if text:
            self.content = types.Content(role="model", parts=[types.Part(text=text)])
        else:
            self.content = None

        if escalate:
            self.actions = MagicMock(escalate=True)
            self.error_message = err
        else:
            self.actions = MagicMock(escalate=False)
            self.error_message = None

    def is_final_response(self) -> bool:
        return self._is_final


@pytest.mark.asyncio
async def test_call_agent_async_successful_response():
    """Verify call_agent_async extracts final response text."""
    runner = MagicMock()

    async def mock_run_async(*args, **kwargs):
        yield MockEvent(is_final=False)
        yield MockEvent(is_final=True, text="This is the final generated response.")

    runner.run_async = mock_run_async

    response = await call_agent_async(
        query="Test query",
        runner=runner,
        user_id="u1",
        session_id="s1",
    )

    assert response == "This is the final generated response."


@pytest.mark.asyncio
async def test_call_agent_async_escalation():
    """Verify call_agent_async properly formats escalation errors."""
    runner = MagicMock()

    async def mock_run_async(*args, **kwargs):
        yield MockEvent(is_final=True, escalate=True, err="Quota exceeded")

    runner.run_async = mock_run_async

    response = await call_agent_async(
        query="Test query",
        runner=runner,
        user_id="u1",
        session_id="s1",
    )

    assert "Agent escalated: Quota exceeded" in response
