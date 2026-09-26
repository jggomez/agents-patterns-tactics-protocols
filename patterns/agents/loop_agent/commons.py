"""Backward-compatibility module re-exporting from patterns.agents.common."""

from __future__ import annotations

try:
    from patterns.agents.common import call_agent_async, get_runner
except ModuleNotFoundError:
    from agents.common import call_agent_async, get_runner

__all__ = ["call_agent_async", "get_runner"]
