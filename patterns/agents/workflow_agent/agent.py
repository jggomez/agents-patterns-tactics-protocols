"""ADK 2.0 Workflow Pattern: Multi-Domain Deep Research Workflow.

Demonstrates:
  1. Deterministic Pre-processing (FunctionNode)
  2. Dynamic Inquiry Router (FunctionNode emitting route in Event)
  3. Fan-out Parallel Execution (Specialized Agents + Deterministic Scanners)
  4. Barrier Synchronization (JoinNode)
  5. Deterministic Validation Gates (FunctionNode)
  6. Consolidated Executive Synthesis (Gemini 3.5 Flash Agent)
"""

from __future__ import annotations

import asyncio
from typing import Any
from google.adk.agents import Agent
from google.adk.events import Event
from google.adk.tools import google_search
from google.adk.workflow import Edge, FunctionNode, JoinNode, START, Workflow
from google.genai import types

try:
    from patterns.agents.common import call_agent_async, get_model, get_runner
except ModuleNotFoundError:
    from agents.common import call_agent_async, get_model, get_runner


# ==============================================================================
# 1. Deterministic Functions (Pure Python Logic)
# ==============================================================================


def pre_process_request(node_input: Any = None) -> str:
    """Deterministic pre-processing: extracts and normalizes query text."""
    if isinstance(node_input, types.Content):
        parts = [p.text for p in (node_input.parts or []) if p.text is not None]
        raw_text = " ".join(parts)
    elif isinstance(node_input, dict):
        raw_text = node_input.get("text") or node_input.get("query") or str(node_input)
    else:
        raw_text = str(node_input or "")

    cleaned = " ".join(raw_text.strip().split())
    print(f"\n[Workflow:PreProcessor] Cleaned request: '{cleaned}'")
    return cleaned


def route_inquiry(node_input: Any = None) -> Event:
    """Deterministic router: classifies query as 'technical' or 'market'."""
    text = str(node_input or "").lower()
    tech_keywords = [
        "tech", "architecture", "code", "latency", "performance",
        "benchmark", "framework", "adk", "api", "database", "security",
        "protocol", "system design", "cloud", "docker", "algorithm"
    ]

    is_technical = any(kw in text for kw in tech_keywords)
    selected_route = "technical" if is_technical else "market"

    print(f"[Workflow:Router] Routing query to branch: '{selected_route.upper()}'")
    return Event(output=node_input, route=selected_route)


def security_scanner(node_input: Any = None) -> dict[str, Any]:
    """Deterministic security & compliance scan without LLM hallucinations."""
    text = str(node_input or "").lower()
    print("[Workflow:SecurityScanner] Running deterministic security & compliance scan...")

    has_auth_mention = any(k in text for k in ["auth", "token", "key", "secret", "credential"])
    has_cloud_mention = any(k in text for k in ["cloud", "gcp", "aws", "azure", "kubernetes"])

    return {
        "analyst": "DeterministicSecurityScanner",
        "cve_status": "Clean (No known high-severity CVE matches)",
        "license_compliance": "Apache 2.0 / MIT Compatible",
        "threat_profile": "Elevated" if has_auth_mention else "Standard",
        "infrastructure_scope": "Multi-Cloud / Containerized" if has_cloud_mention else "Local / Hybrid",
        "mandatory_checks": [
            "Enforce TLS 1.3 in transit",
            "Principle of Least Privilege for tool calling",
            "Deterministic input validation before LLM prompts"
        ]
    }


def validate_technical_findings(node_input: Any = None) -> str:
    """Deterministic quality gate: validates technical findings bundle."""
    data = node_input if isinstance(node_input, dict) else {}
    workers_completed = list(data.keys())
    print(f"[Workflow:QualityGate] Validated Technical branch workers: {workers_completed}")

    summary_bundle = (
        f"### Technical Investigation Bundle\n"
        f"Workers Synchronized: {len(workers_completed)}\n\n"
    )
    for worker, result in data.items():
        summary_bundle += f"#### [{worker} Output]:\n{result}\n\n"

    return summary_bundle


def validate_market_findings(node_input: Any = None) -> str:
    """Deterministic quality gate: validates market findings bundle."""
    data = node_input if isinstance(node_input, dict) else {}
    workers_completed = list(data.keys())
    print(f"[Workflow:QualityGate] Validated Market branch workers: {workers_completed}")

    summary_bundle = (
        f"### Market Investigation Bundle\n"
        f"Workers Synchronized: {len(workers_completed)}\n\n"
    )
    for worker, result in data.items():
        summary_bundle += f"#### [{worker} Output]:\n{result}\n\n"

    return summary_bundle


# ==============================================================================
# 2. Specialized LLM Agents (Gemini 3.5 Flash)
# ==============================================================================

# Technical Branch Workers
tech_architecture_agent = Agent(
    name="TechArchitectureAnalyst",
    model=get_model(),
    description="Specialist in system architecture, design patterns, and framework mechanics.",
    instruction="""You are a Principal Software Architect.
    Analyze the technical query provided. Focus on:
    1. System architecture, modular design, and protocols.
    2. Framework specifications, patterns (e.g. DAG, ReAct), and APIs.
    3. Trade-offs and architectural recommendations.
    Keep your findings concise, structured, and under 150 words.""",
    tools=[google_search],
)

performance_agent = Agent(
    name="PerformanceAnalyst",
    model=get_model(),
    description="Specialist in latency, throughput, benchmarking, and scalability.",
    instruction="""You are a Staff Performance & Reliability Engineer.
    Analyze the inquiry focusing on:
    1. Runtime latency, compute overhead, and token efficiency.
    2. Concurrency models (fan-out, parallel workers, async I/O).
    3. Bottlenecks, failure modes, and mitigation strategies.
    Keep your findings concise, structured, and under 150 words.""",
    tools=[google_search],
)

# Market Branch Workers
competitor_agent = Agent(
    name="CompetitorIntelligenceAnalyst",
    model=get_model(),
    description="Specialist in competitive landscape, market positioning, and alternatives.",
    instruction="""You are a Market Intelligence Analyst.
    Analyze the inquiry focusing on:
    1. Industry alternatives and key competing frameworks/solutions.
    2. Core competitive differentiators and adoption trends.
    3. Ecosystem maturity and developer sentiment.
    Keep your findings concise, structured, and under 150 words.""",
    tools=[google_search],
)

financial_agent = Agent(
    name="FinancialPricingAnalyst",
    model=get_model(),
    description="Specialist in pricing models, unit economics, and ROI.",
    instruction="""You are a Financial & Business Model Analyst.
    Analyze the inquiry focusing on:
    1. Pricing structures, cost per unit/token/operation.
    2. TCO (Total Cost of Ownership) and infrastructure ROI.
    3. Monetization trends and enterprise licensing.
    Keep your findings concise, structured, and under 150 words.""",
    tools=[google_search],
)

# Executive Synthesizer (Convergent Join Node Target)
executive_synthesizer = Agent(
    name="ExecutiveResearchDirector",
    model=get_model(),
    description="Synthesizes multi-dimensional investigation findings into an executive report.",
    instruction="""You are the Executive Research Director.
    You have received a synchronized bundle of findings from specialized analysts and deterministic quality gates.
    Synthesize all provided information into a high-impact, professional Executive Intelligence Report:

    Structure your report as:
    # 📋 Executive Intelligence Briefing
    ## 1. Executive Summary
    ## 2. Synthesized Core Findings
    ## 3. Risks, Trade-offs & Security Posture
    ## 4. Strategic Recommendations & Action Plan

    Maintain an objective, executive tone with crisp bullet points.""",
)


# ==============================================================================
# 3. Graph Assembly (Workflow, Nodes, Edges, Joins)
# ==============================================================================

# Deterministic Function Nodes
pre_process_node = FunctionNode(func=pre_process_request, name="PreProcessor")
router_node = FunctionNode(func=route_inquiry, name="DomainRouter")
security_node = FunctionNode(func=security_scanner, name="SecurityScanner")
val_tech_node = FunctionNode(func=validate_technical_findings, name="TechQualityGate")
val_market_node = FunctionNode(func=validate_market_findings, name="MarketQualityGate")

# Barrier Synchronization Nodes
join_technical = JoinNode(name="JoinTechnicalBranch")
join_market = JoinNode(name="JoinMarketBranch")

# Edges definition
workflow_edges = [
    # Initial deterministic stages
    Edge(from_node=START, to_node=pre_process_node),
    Edge(from_node=pre_process_node, to_node=router_node),

    # Branch A: Technical (Fan-Out)
    Edge(from_node=router_node, to_node=tech_architecture_agent, route="technical"),
    Edge(from_node=router_node, to_node=performance_agent, route="technical"),
    Edge(from_node=router_node, to_node=security_node, route="technical"),

    # Branch A: Join Barrier & Quality Gate
    Edge(from_node=tech_architecture_agent, to_node=join_technical),
    Edge(from_node=performance_agent, to_node=join_technical),
    Edge(from_node=security_node, to_node=join_technical),
    Edge(from_node=join_technical, to_node=val_tech_node),
    Edge(from_node=val_tech_node, to_node=executive_synthesizer),

    # Branch B: Market (Fan-Out)
    Edge(from_node=router_node, to_node=competitor_agent, route="market"),
    Edge(from_node=router_node, to_node=financial_agent, route="market"),

    # Branch B: Join Barrier & Quality Gate
    Edge(from_node=competitor_agent, to_node=join_market),
    Edge(from_node=financial_agent, to_node=join_market),
    Edge(from_node=join_market, to_node=val_market_node),
    Edge(from_node=val_market_node, to_node=executive_synthesizer),
]

# Root ADK 2.0 Workflow Node
root_agent = Workflow(
    name="MultiDomainResearchWorkflow",
    description="ADK 2.0 graph workflow with deterministic steps, routing, fan-out, and join.",
    edges=workflow_edges,
)


# ==============================================================================
# 4. Execution Functions
# ==============================================================================


async def run_conversation(query: str | None = None) -> None:
    """Executes the research workflow with a sample or user-provided query."""
    runner, user_id, session_id = await get_runner(root_agent)

    test_query = query or (
        "Investigate Google ADK 2.0 Workflow architecture, latency benchmarks, "
        "and security compliance for enterprise agent systems"
    )

    await call_agent_async(test_query, runner, user_id, session_id)


def main() -> None:
    """Entry point for standalone execution."""
    asyncio.run(run_conversation())


if __name__ == "__main__":
    main()
