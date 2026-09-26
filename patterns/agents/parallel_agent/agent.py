"""Parallel Agent: Concurrent execution of specialized researchers aggregated by an executive agent."""

from __future__ import annotations

import asyncio
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

try:
    from patterns.agents.common import call_agent_async, get_model, get_runner
except ModuleNotFoundError:
    from agents.common import call_agent_async, get_model, get_runner

# Tech Researcher: Focuses on AI and ML trends
tech_researcher = Agent(
    name="TechResearcher",
    model=get_model(),
    instruction="""Research the latest AI/ML trends. Include 3 key developments,
    the main companies involved, and the potential impact. Keep the report very concise (100 words).""",
    tools=[google_search],
    output_key="tech_research",
)

# Health Researcher: Focuses on medical breakthroughs
health_researcher = Agent(
    name="HealthResearcher",
    model=get_model(),
    instruction="""Research recent medical breakthroughs. Include 3 significant advances,
    their practical applications, and estimated timelines. Keep the report concise (100 words).""",
    tools=[google_search],
    output_key="health_research",
)

# Finance Researcher: Focuses on fintech trends
finance_researcher = Agent(
    name="FinanceResearcher",
    model=get_model(),
    instruction="""Research current fintech trends. Include 3 key trends,
    their market implications, and the future outlook. Keep the report concise (100 words).""",
    tools=[google_search],
    output_key="finance_research",
)

# Aggregator Agent: Synthesizes findings from parallel researchers
aggregator_agent = Agent(
    name="AggregatorAgent",
    model=get_model(),
    instruction="""Combine these three research findings into a single executive summary:

    **Technology Trends:**
    {tech_research}

    **Health Breakthroughs:**
    {health_research}

    **Finance Innovations:**
    {finance_research}

    Your summary should highlight common themes, surprising connections, and the most important key takeaways from all three reports. The final summary should be around 200 words.""",
    output_key="executive_summary",
)

# Parallel research team running concurrently
parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[tech_researcher, health_researcher, finance_researcher],
)

# Root pipeline: Run parallel team first, then aggregate
root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[parallel_research_team, aggregator_agent],
)


async def run_conversation() -> None:
    """Executes the parallel research workflow."""
    runner, user_id, session_id = await get_runner(root_agent)
    await call_agent_async(
        "Run the daily executive briefing on Tech, Health, and Finance",
        runner,
        user_id,
        session_id,
    )


def main() -> None:
    """Entry point for direct script execution."""
    asyncio.run(run_conversation())


if __name__ == "__main__":
    main()
