"""Loop Agent: Iterative refinement with critic-refiner feedback cycle."""

from __future__ import annotations

import asyncio
from typing import Any
from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.tools import FunctionTool

try:
    from patterns.agents.common import call_agent_async, get_model, get_runner
except ModuleNotFoundError:
    from agents.common import call_agent_async, get_model, get_runner

# Initial Writer: Generates the first draft
initial_writer_agent = Agent(
    name="InitialWriterAgent",
    model=get_model(),
    instruction="""Based on the user's prompt, write the first draft of a short story (around 100-150 words).
    Output only the story text, with no introduction or explanation.""",
    output_key="current_story",
)

# Critic Agent: Evaluates draft and signals approval or improvement points
critic_agent = Agent(
    name="CriticAgent",
    model=get_model(),
    instruction="""You are a constructive story critic. Review the story provided below.
    Story: {current_story}

    Evaluate the story's plot, characters, and pacing.
    - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
    - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
    output_key="critique",
)


def exit_loop() -> dict[str, str]:
    """Call this function ONLY when the critique is 'APPROVED', indicating the story is finished."""
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}


# Refiner Agent: Incorporates feedback or triggers loop termination
refiner_agent = Agent(
    name="RefinerAgent",
    model=get_model(),
    instruction="""You are a story refiner. You have a story draft and critique.

    Story Draft: {current_story}
    Critique: {critique}

    Your task is to analyze the critique:
    - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` tool.
    - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
    output_key="current_story",
    tools=[FunctionTool(exit_loop)],
)

# Iterative refinement loop: Runs Critic -> Refiner up to max_iterations
story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2,
)

# Root pipeline: First write, then enter refinement loop
root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[initial_writer_agent, story_refinement_loop],
)


async def run_conversation() -> None:
    """Executes the iterative story refinement workflow."""
    runner, user_id, session_id = await get_runner(root_agent)
    await call_agent_async(
        "Write a short story about a lighthouse keeper who discovers a mysterious, glowing map",
        runner,
        user_id,
        session_id,
    )


def main() -> None:
    """Entry point for direct script execution."""
    asyncio.run(run_conversation())


if __name__ == "__main__":
    main()
