"""Multi-agent pattern implementations."""

from .first_agent.agent import root_agent as first_agent
from .sequential_agent.agent import root_agent as sequential_agent
from .parallel_agent.agent import root_agent as parallel_agent
from .orchestrator_agent.agent import root_agent as orchestrator_agent
from .loop_agent.agent import root_agent as loop_agent
from .workflow_agent.agent import root_agent as workflow_agent

__all__ = [
    "first_agent",
    "sequential_agent",
    "parallel_agent",
    "orchestrator_agent",
    "loop_agent",
    "workflow_agent",
]
