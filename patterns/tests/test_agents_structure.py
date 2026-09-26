"""Structural verification tests for all 5 ADK Agent Patterns."""

import pytest
from google.adk.agents import Agent, LoopAgent, ParallelAgent, SequentialAgent
from google.adk.tools import AgentTool

from patterns.agents.first_agent.agent import root_agent as first_agent
from patterns.agents.sequential_agent.agent import root_agent as sequential_agent
from patterns.agents.parallel_agent.agent import root_agent as parallel_agent
from patterns.agents.orchestrator_agent.agent import root_agent as orchestrator_agent
from patterns.agents.loop_agent.agent import root_agent as loop_agent


def test_first_agent_structure():
    """Verify first_agent definition and tool configuration."""
    assert first_agent.name == "helpful_assistant"
    assert len(first_agent.tools) == 1
    assert "Search" in first_agent.instruction or "helpful" in first_agent.instruction


def test_sequential_agent_structure():
    """Verify sequential_agent pipeline and chained keys."""
    assert isinstance(sequential_agent, SequentialAgent)
    assert sequential_agent.name == "BlogPipeline"
    assert len(sequential_agent.sub_agents) == 3

    outline_ag, writer_ag, editor_ag = sequential_agent.sub_agents
    assert outline_ag.name == "OutlineAgent"
    assert outline_ag.output_key == "blog_outline"

    assert writer_ag.name == "WriterAgent"
    assert writer_ag.output_key == "blog_draft"
    assert "{blog_outline}" in writer_ag.instruction

    assert editor_ag.name == "EditorAgent"
    assert editor_ag.output_key == "final_blog"
    assert "{blog_draft}" in editor_ag.instruction


def test_parallel_agent_structure():
    """Verify parallel_agent researchers and executive aggregator."""
    assert isinstance(parallel_agent, SequentialAgent)
    assert parallel_agent.name == "ResearchSystem"
    assert len(parallel_agent.sub_agents) == 2

    parallel_team, aggregator = parallel_agent.sub_agents
    assert isinstance(parallel_team, ParallelAgent)
    assert parallel_team.name == "ParallelResearchTeam"
    assert len(parallel_team.sub_agents) == 3

    researcher_names = [agent.name for agent in parallel_team.sub_agents]
    assert "TechResearcher" in researcher_names
    assert "HealthResearcher" in researcher_names
    assert "FinanceResearcher" in researcher_names

    assert aggregator.name == "AggregatorAgent"
    assert "{tech_research}" in aggregator.instruction
    assert "{health_research}" in aggregator.instruction
    assert "{finance_research}" in aggregator.instruction


def test_orchestrator_agent_structure():
    """Verify orchestrator Agent-as-Tool composition."""
    assert orchestrator_agent.name == "ResearchCoordinator"
    assert len(orchestrator_agent.tools) == 2

    tool_names = [getattr(t, "name", str(t)) for t in orchestrator_agent.tools]
    assert any("ResearchAgent" in name for name in tool_names)
    assert any("SummarizerAgent" in name for name in tool_names)


def test_loop_agent_structure():
    """Verify loop_agent cycle and max_iterations limit."""
    assert isinstance(loop_agent, SequentialAgent)
    assert loop_agent.name == "StoryPipeline"
    assert len(loop_agent.sub_agents) == 2

    initial_writer, loop_refiner = loop_agent.sub_agents
    assert initial_writer.name == "InitialWriterAgent"
    assert isinstance(loop_refiner, LoopAgent)
    assert loop_refiner.name == "StoryRefinementLoop"
    assert loop_refiner.max_iterations == 2

    critic, refiner = loop_refiner.sub_agents
    assert critic.name == "CriticAgent"
    assert refiner.name == "RefinerAgent"
    assert len(refiner.tools) == 1


def test_backward_compatibility_reexports():
    """Verify backward-compatible commons.py in all agent folders."""
    from patterns.agents.first_agent.commons import call_agent_async as c1, get_runner as r1
    from patterns.agents.sequential_agent.commons import call_agent_async as c2, get_runner as r2
    from patterns.agents.parallel_agent.commons import call_agent_async as c3, get_runner as r3
    from patterns.agents.orchestrator_agent.commons import call_agent_async as c4, get_runner as r4
    from patterns.agents.loop_agent.commons import call_agent_async as c5, get_runner as r5

    assert callable(c1) and callable(r1)
    assert callable(c2) and callable(r2)
    assert callable(c3) and callable(r3)
    assert callable(c4) and callable(r4)
    assert callable(c5) and callable(r5)
