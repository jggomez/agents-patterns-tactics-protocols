"""Sequential Agent: Linear pipeline chaining Outline -> Writer -> Editor."""

from __future__ import annotations

import asyncio
from google.adk.agents import Agent, SequentialAgent

try:
    from patterns.agents.common import call_agent_async, get_model, get_runner
except ModuleNotFoundError:
    from agents.common import call_agent_async, get_model, get_runner

# Outline Agent: Generates structured blog outline
outline_agent = Agent(
    name="OutlineAgent",
    model=get_model(),
    instruction="""Create a blog outline for the given topic with:
    1. A catchy headline
    2. An introduction hook
    3. 3-5 main sections with 2-3 bullet points for each
    4. A concluding thought""",
    output_key="blog_outline",
)

# Writer Agent: Writes full draft based on {blog_outline}
writer_agent = Agent(
    name="WriterAgent",
    model=get_model(),
    instruction="""Following this outline strictly: {blog_outline}
    Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
    output_key="blog_draft",
)

# Editor Agent: Polishes draft from {blog_draft}
editor_agent = Agent(
    name="EditorAgent",
    model=get_model(),
    instruction="""Edit this draft: {blog_draft}
    Your task is to polish the text by fixing any grammatical errors, improving the flow and sentence structure, and enhancing overall clarity.""",
    output_key="final_blog",
)

# Root Sequential Pipeline
root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent],
)


async def run_conversation() -> None:
    """Executes the sequential blog writing pipeline."""
    runner, user_id, session_id = await get_runner(root_agent)
    await call_agent_async(
        "Write a blog post about the benefits of multi-agent systems for software developers",
        runner,
        user_id,
        session_id,
    )


def main() -> None:
    """Entry point for direct script execution."""
    asyncio.run(run_conversation())


if __name__ == "__main__":
    main()
