# AI Agent Workflow Patterns with Google ADK

This directory explores classic agent workflow patterns implemented using the **Google Agent Development Kit (ADK)** and **Gemini 3.5 Flash**. These patterns demonstrate different ways to coordinate multiple agents or structure complex workflows.

## 📂 Structure

The patterns are organized under a centralized architecture managed by `uv`:

```
patterns/
├── pyproject.toml           # Project dependencies & tool configurations (uv)
├── uv.lock                  # Deterministic dependency lockfile
├── .env.example             # Environment variable template
├── run.sh                   # Interactive shell to run & verify agents
├── verify.py                # Self-diagnostic health check script
├── cli.py                   # Unified CLI entry point
├── tests/                   # Automated pytest suite
│   ├── test_common.py
│   ├── test_agents_structure.py
│   ├── test_execution_mock.py
│   └── test_workflow.py
└── agents/
    ├── __init__.py
    ├── common/              # Centralized configuration & runner
    │   ├── config.py        # Gemini 3.5 Flash & retry policies
    │   └── runner.py        # Session management & ADK runner
    ├── first_agent/         # Basic conversational agent with tool integration
    ├── loop_agent/          # Iterative refinement with feedback loops
    ├── orchestrator_agent/  # Dynamic coordination using the Agent-as-Tool pattern
    ├── parallel_agent/      # Concurrent execution for multi-faceted tasks
    ├── sequential_agent/    # Linear pipelines for multi-stage workflows
    └── workflow_agent/      # ADK 2.0 Graph Workflow (Deterministic, Router, Fan-Out, Join)
```

## 🎯 Orchestration Patterns

### 1. The Simple Agent (`first_agent`)
A standalone agent that uses tools to solve a task. It demonstrates the basic building blocks: instructions, models, and function calling.
- **Use Case:** Simple info retrieval, single-task automation.

### 2. Sequential Workflow (`sequential_agent`)
A linear pipeline where the output of one agent serves as the input (or part of the context) for the next.
- **Implementation:** Uses `SequentialAgent` to coordinate a chain of specialists.
- **Use Case:** Blog generation (Outline -> Write -> Edit).

### 3. Orchestrator (Agent-as-Tool) (`orchestrator_agent`)
A root "Coordinator" agent that has access to other agents as tools. It dynamically decides which specialist to call and when.
- **Implementation:** Uses `AgentTool` to wrap sub-agents.
- **Use Case:** Research & Summarization, Executive Briefings.

### 4. Parallel Workflow (`parallel_agent`)
Runs multiple agents or tool-calls concurrently to gather information or perform tasks in parallel, improving latency and separation of concerns.
- **Use Case:** Multi-source research, multi-departmental support queries.

### 5. Loop / Iterative Refinement (`loop_agent`)
An agent that iteratively reviews and improves its own output (or the output of others) until a certain condition or quality bar is met.
- **Use Case:** Code debugging, story refinement, translation optimization.

### 6. Graph Workflow (ADK 2.0) (`workflow_agent`)
A directed acyclic graph (DAG) workflow combining deterministic processing steps, dynamic routing, parallel execution (fan-out), quality gate validation, and barrier synchronization (join).
- **Implementation:** Uses native Google ADK 2.0 `Workflow`, `FunctionNode`, `JoinNode`, and conditional `Edge(route=...)`.
- **Flow:**
  1. **Deterministic Sanitizer & Classifier:** Preprocesses query and extracts domain keywords (`FunctionNode`).
  2. **Deterministic Route Selector:** Evaluates metadata and emits route events (`technical` vs `market`).
  3. **Fan-Out Branches:**
     - *Technical Branch:* Concurrent `Security Compliance Scanner` (deterministic AST/pattern check), `Cloud Architect Agent`, and `Performance Specialist Agent`. Output verified by a deterministic Quality Gate (`validate_technical_findings`).
     - *Market Branch:* Concurrent `Competitor Analyst Agent` and `Financial Analyst Agent`. Output verified by a deterministic Quality Gate (`validate_market_findings`).
  4. **Barrier Join (`JoinNode`):** Synchronizes concurrent branch executions into a unified structured dictionary.
  5. **Executive Synthesizer Agent:** Synthesizes the finalized multi-domain executive report.
- **Use Case:** Multi-domain enterprise research, policy-governed agent pipelines, deterministic validation gates.

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
cd patterns

# Copy environment template
cp .env.example .env

# Set your GEMINI_API_KEY in .env
```

### 2. Interactive Shell Runner
Launch the interactive shell menu:
```bash
./run.sh
```

Or run any pattern directly:
```bash
./run.sh first          # Run Simple Agent
./run.sh sequential     # Run Sequential Agent
./run.sh parallel       # Run Parallel Agent
./run.sh orchestrator   # Run Orchestrator Agent
./run.sh loop           # Run Loop Agent
./run.sh workflow       # Run ADK 2.0 Graph Workflow Agent
```

### 3. Diagnostics & Verification
Run the self-diagnostic suite:
```bash
./run.sh verify         # Runs health check, import validation, and tests
./run.sh test           # Runs pytest suite directly
```

---

## 🔑 Key Concepts Covered

- **Gemini 3.5 Flash**: Default model across all agents, configurable via `GEMINI_MODEL`.
- **ADK 2.0 Graph Workflows**: Native DAG orchestration with `Workflow`, `FunctionNode`, `JoinNode`, and dynamic event-based routing.
- **Centralized Commons**: Shared configuration and runner lifecycle in `agents/common/`.
- **Reliable Imports**: Robust namespace imports with fallback compatibility.
- **Automated Verification**: Comprehensive structural and mock execution tests.
