"""Orchestrator Agent: Dynamic workflow coordination using the Agent-as-Tool pattern."""

from __future__ import annotations

import asyncio
from google.adk.agents import Agent
from google.adk.tools import AgentTool, google_search

try:
    from patterns.agents.common import call_agent_async, get_model, get_runner
except ModuleNotFoundError:
    from agents.common import call_agent_async, get_model, get_runner

# Research Agent: Gathers facts using Google Search
research_agent = Agent(
    name="ResearchAgent",
    model=get_model(),
    instruction="""You are a specialized research agent. Your only job is to use the
    google_search tool to find 2-3 pieces of relevant information on the given topic and 
    present the findings with citations.""",
    tools=[google_search],
    output_key="research_findings",
)

# Summarizer Agent: Synthesizes input into structured bullet points
summarizer_agent = Agent(
    name="SummarizerAgent",
    model=get_model(),
    instruction="""Read the provided research findings: {research_findings} 
    Create a concise summary as a bulleted list with 3-5 key points.""",
    output_key="final_summary",
)

# Root Coordinator: Dynamic router calling sub-agents via AgentTool
root_agent = Agent(
    name="ResearchCoordinator",
    model=get_model(),
    instruction="""You are a research coordinator.
    Your goal is to answer the user's query by orchestrating a workflow:
    1. First, call the `ResearchAgent` tool to find relevant information on the topic provided by the user.
    2. Next, after receiving the research findings, call the `SummarizerAgent` tool to create a concise summary.
    3. Finally, present the final summary clearly to the user as your response.""",
    tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
)


async def run_conversation() -> None:
    """Executes the orchestrator agent workflow."""
    runner, user_id, session_id = await get_runner(root_agent)
    await call_agent_async(
        "What are the latest advancements in quantum computing and what do they mean for AI?",
        runner,
        user_id,
        session_id,
    )


def main() -> None:
    """Entry point for direct script execution."""
    asyncio.run(run_conversation())


if __name__ == "__main__":
    main()
