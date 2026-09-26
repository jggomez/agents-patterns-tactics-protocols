"""First Agent: Standalone conversational agent with Google Search tool."""

from __future__ import annotations

import asyncio
from google.adk.agents import Agent
from google.adk.tools import google_search

try:
    from patterns.agents.common import call_agent_async, get_model, get_runner
except ModuleNotFoundError:
    from agents.common import call_agent_async, get_model, get_runner

# Define the root conversational agent using the centralized model
root_agent = Agent(
    name="helpful_assistant",
    model=get_model(),
    description="A simple agent that can answer general questions using Google Search.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)


async def run_conversation() -> None:
    """Executes a sample conversational session with sequential queries."""
    runner, user_id, session_id = await get_runner(root_agent)
    await call_agent_async("What is the weather like in CDMX?", runner, user_id, session_id)
    await call_agent_async("How about Monterrey?", runner, user_id, session_id)
    await call_agent_async("Tell me the weather in Puebla", runner, user_id, session_id)


def main() -> None:
    """Entry point for direct script execution."""
    asyncio.run(run_conversation())


if __name__ == "__main__":
    main()
