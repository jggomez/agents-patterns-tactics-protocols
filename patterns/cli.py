"""Unified CLI for executing ADK Agent Patterns."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Ensure patterns directory and parent repository are on sys.path
BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from patterns.agents.first_agent.agent import run_conversation as run_first
    from patterns.agents.sequential_agent.agent import run_conversation as run_sequential
    from patterns.agents.parallel_agent.agent import run_conversation as run_parallel
    from patterns.agents.orchestrator_agent.agent import run_conversation as run_orchestrator
    from patterns.agents.loop_agent.agent import run_conversation as run_loop
    from patterns.agents.workflow_agent.agent import run_conversation as run_workflow
except ModuleNotFoundError:
    from agents.first_agent.agent import run_conversation as run_first
    from agents.sequential_agent.agent import run_conversation as run_sequential
    from agents.parallel_agent.agent import run_conversation as run_parallel
    from agents.orchestrator_agent.agent import run_conversation as run_orchestrator
    from agents.loop_agent.agent import run_conversation as run_loop
    from agents.workflow_agent.agent import run_conversation as run_workflow

AGENTS = {
    "first": ("Simple Agent with Google Search", run_first),
    "sequential": ("Sequential Pipeline (Outline -> Write -> Edit)", run_sequential),
    "parallel": ("Parallel Research Team + Aggregator", run_parallel),
    "orchestrator": ("Dynamic Orchestrator with Agent-as-Tool", run_orchestrator),
    "loop": ("Iterative Refinement Loop (Writer -> Critic -> Refiner)", run_loop),
    "workflow": ("ADK 2.0 Graph Workflow (Deterministic, Router, Fan-Out, Join)", run_workflow),
}


def print_banner(agent_key: str) -> None:
    title, _ = AGENTS[agent_key]
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    print("=" * 60)
    print(f"🚀 Running Pattern: {agent_key.upper()} ({title})")
    print(f"🤖 Gemini Model:   {model_name}")
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Unified CLI runner for Google ADK Agent Patterns"
    )
    parser.add_argument(
        "agent",
        choices=list(AGENTS.keys()) + ["list"],
        help="The agent pattern to execute (or 'list' to view available patterns)",
    )

    args = parser.parse_args()

    if args.agent == "list":
        print("\nAvailable Agent Patterns:")
        for key, (desc, _) in AGENTS.items():
            print(f"  • {key:<12} : {desc}")
        print()
        return

    print_banner(args.agent)
    _, run_func = AGENTS[args.agent]
    asyncio.run(run_func())


if __name__ == "__main__":
    main()
