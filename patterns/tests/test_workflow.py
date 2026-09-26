"""Unit and structural tests for ADK 2.0 Multi-Domain Research Workflow."""

import pytest
from google.adk.workflow import Workflow, JoinNode, FunctionNode, START
from google.genai import types

from patterns.agents.workflow_agent.agent import (
    root_agent as workflow_agent,
    pre_process_request,
    route_inquiry,
    security_scanner,
    validate_technical_findings,
    validate_market_findings,
    tech_architecture_agent,
    performance_agent,
    competitor_agent,
    financial_agent,
    executive_synthesizer,
    join_technical,
    join_market,
)


def test_workflow_graph_structure():
    """Verify that root_agent is a valid ADK 2.0 Workflow DAG."""
    assert isinstance(workflow_agent, Workflow)
    assert workflow_agent.name == "MultiDomainResearchWorkflow"

    # Validate the DAG topology
    workflow_agent.graph.validate_graph()

    # Verify single terminal node
    assert workflow_agent.graph._terminal_node_names == {"ExecutiveResearchDirector"}

    # Verify nodes present in graph
    node_names = [n.name for n in workflow_agent.graph.nodes]
    assert "PreProcessor" in node_names
    assert "DomainRouter" in node_names
    assert "TechArchitectureAnalyst" in node_names
    assert "PerformanceAnalyst" in node_names
    assert "SecurityScanner" in node_names
    assert "JoinTechnicalBranch" in node_names
    assert "TechQualityGate" in node_names
    assert "CompetitorIntelligenceAnalyst" in node_names
    assert "FinancialPricingAnalyst" in node_names
    assert "JoinMarketBranch" in node_names
    assert "MarketQualityGate" in node_names
    assert "ExecutiveResearchDirector" in node_names


def test_deterministic_preprocessor():
    """Verify query normalization and whitespace stripping."""
    raw = "   Investigate   ADK  2.0   latency  and   benchmarks   \n"
    cleaned = pre_process_request(raw)
    assert cleaned == "Investigate ADK 2.0 latency and benchmarks"

    # Test with Content object
    content = types.Content(role="user", parts=[types.Part(text="  Test query  ")])
    assert pre_process_request(content) == "Test query"


def test_deterministic_router():
    """Verify conditional routing between 'technical' and 'market'."""
    tech_event = route_inquiry("Analyze system architecture and latency benchmarks")
    assert tech_event.actions.route == "technical"

    market_event = route_inquiry("Analyze startup competitors, pricing, and market share")
    assert market_event.actions.route == "market"


def test_deterministic_security_scanner():
    """Verify pure Python security/compliance audit logic."""
    res = security_scanner("Check cloud authentication credentials")
    assert res["threat_profile"] == "Elevated"
    assert res["infrastructure_scope"] == "Multi-Cloud / Containerized"
    assert "Clean" in res["cve_status"]
    assert len(res["mandatory_checks"]) >= 3


def test_deterministic_quality_gates():
    """Verify bundling and validation formatting in quality gates."""
    tech_inputs = {
        "TechArchitectureAnalyst": "Modular design verified.",
        "PerformanceAnalyst": "Latency p95 < 200ms.",
        "SecurityScanner": {"cve": "none"},
    }
    tech_bundle = validate_technical_findings(tech_inputs)
    assert "Technical Investigation Bundle" in tech_bundle
    assert "Workers Synchronized: 3" in tech_bundle

    market_inputs = {
        "CompetitorIntelligenceAnalyst": "Competitor landscape mapped.",
        "FinancialPricingAnalyst": "Unit margin: 68%.",
    }
    market_bundle = validate_market_findings(market_inputs)
    assert "Market Investigation Bundle" in market_bundle
    assert "Workers Synchronized: 2" in market_bundle


def test_join_nodes():
    """Verify that JoinNodes enforce barrier synchronization across all predecessors."""
    assert isinstance(join_technical, JoinNode)
    assert join_technical._requires_all_predecessors is True

    assert isinstance(join_market, JoinNode)
    assert join_market._requires_all_predecessors is True


def test_backward_compatibility_commons():
    """Verify workflow_agent/commons.py re-export."""
    from patterns.agents.workflow_agent.commons import call_agent_async, get_runner
    assert callable(call_agent_async)
    assert callable(get_runner)
