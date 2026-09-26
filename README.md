# Workshop: AI Agent Patterns & Interoperability Protocols

A comprehensive hands-on workshop exploring the design, orchestration, and standardization of AI Agents. This repository demonstrates how to build modular, autonomous, and interoperable agentic systems using the **Google Agent Development Kit (ADK)**, **Gemini 3.5 Flash**, and modern industry protocols.

---

## 📂 Repository Architecture

The workshop is organized into two primary technical pillars, alongside presentation resources:

```
├── patterns/                     # Agent Orchestration Patterns (ADK + Gemini 3.5 Flash)
│   ├── agents/
│   │   ├── common/               # Shared configuration, Gemini 3.5 Flash, runner lifecycle
│   │   ├── first_agent/          # Simple conversational agent with tool integration
│   │   ├── sequential_agent/     # Linear multi-stage pipeline
│   │   ├── parallel_agent/       # Concurrent multi-agent execution
│   │   ├── orchestrator_agent/   # Dynamic coordination via Agent-as-Tool
│   │   ├── loop_agent/           # Iterative refinement & feedback loops
│   │   └── workflow_agent/       # Native Google ADK 2.0 Graph Workflow (DAG)
│   ├── run.sh                    # Interactive terminal runner
│   ├── verify.py                 # Self-diagnostic health check
│   └── tests/                    # Automated pytest test suite (19 tests)
│
├── protocols/                    # Interoperability Protocols (MCP, A2A, A2UI, AG-UI)
│   ├── MCP/                      # Model Context Protocol (FastMCP on :8080)
│   ├── A2A/                      # Agent-to-Agent Protocol (A2A SDK on :10000)
│   ├── A2UI/                     # Agent-to-User Interface v0.9 (Lit Web Components on :10001 & :5173)
│   ├── AGUI/                     # CopilotKit Bridge (FastAPI backend :8000 & Next.js frontend :3000)
│   ├── run.sh                    # Interactive runner & multi-service manager
│   └── verify.py                 # Protocol validation & health check
│
└── slides/                       # Workshop Presentation Slides
    ├── Agentic Systems - Patterns - Protocols.pdf
    └── readme.md
```

---

## 🎯 Pillar 1: Agent Orchestration Patterns ([`patterns/`](./patterns))

Explore classic and modern multi-agent design patterns built with `google-adk`:

1. **Simple Agent (`first_agent`)**: Standalone agent utilizing function calling (`FunctionTool`) for single-task automation and search.
2. **Sequential Workflow (`sequential_agent`)**: Linear pipeline passing state and context through specialist agents (Outline -> Write -> Edit).
3. **Parallel Workflow (`parallel_agent`)**: Concurrent multi-agent execution for multi-source research and low-latency analysis.
4. **Orchestrator Pattern (`orchestrator_agent`)**: Dynamic routing where a central coordinator delegates tasks to sub-agents wrapped as tools (`AgentTool`).
5. **Loop / Iterative Refinement (`loop_agent`)**: Self-correcting feedback cycles that critique and improve outputs until quality thresholds are met.
6. **Graph Workflow (`workflow_agent`)**: Native **Google ADK 2.0 Graph Workflow** using directed acyclic graphs (`Workflow`, `FunctionNode`, `JoinNode`, `Edge`), deterministic pre-processing/sanitization, dynamic route selection, parallel fan-out branches, quality gates, and barrier synchronization.

---

## 🌐 Pillar 2: Interoperability Protocols ([`protocols/`](./protocols))

Implement industry-standard protocols that decouple agents from proprietary platforms, tools, and frontends:

| Protocol | Port(s) | Stack | Purpose |
| :--- | :--- | :--- | :--- |
| **[MCP](./protocols/MCP)** | `:8080` | `FastMCP`, `httpx` | Exposes tools and data sources over streamable HTTP SSE (`/mcp`) via the Model Context Protocol. |
| **[A2A](./protocols/A2A)** | `:10000` | `google-adk`, `a2a-sdk` | Agent-to-Agent discovery card (`/.well-known/agent.json`) and task-oriented JSON-RPC communication. |
| **[A2UI](./protocols/A2UI)** | `:10001`<br/>`:5173` | Backend: ADK + A2A<br/>Frontend: Lit + `@a2ui/lit` v0.9 | Official **A2UI Protocol v0.9 (Prompt-First Architecture)** with `createSurface`, `updateDataModel`, and `updateComponents`. |
| **[AG-UI](./protocols/AGUI)** | `:8000`<br/>`:3000` | Backend: `ag-ui-adk` + FastAPI<br/>Frontend: Next.js 16 + CopilotKit | Real-time event streaming bridge connecting ADK agents directly to CopilotKit React copilot sidebars and popups. |

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python**: `>=3.10` (managed via [`uv`](https://github.com/astral-sh/uv))
- **Node.js**: `>=20.0.0` with npm
- **API Key**: Gemini Developer API Key (`GEMINI_API_KEY`) or Google Cloud Vertex AI credentials.

### 1. Interactive Patterns Shell
```bash
cd patterns

# Configure API key
cp .env.example .env
# Edit .env and set GEMINI_API_KEY=your_key_here

# Launch interactive menu
./run.sh

# Or run tests & diagnostics directly:
./run.sh test       # Runs 19 automated pytest tests
./run.sh verify     # Runs health checks & agent import verification
./run.sh workflow   # Runs ADK 2.0 Graph Workflow agent
```

### 2. Interactive Protocols Shell
```bash
cd protocols

# Run full protocol diagnostic
./run.sh verify

# Start services individually or test:
./run.sh mcp              # Start FastMCP server (:8080)
./run.sh mcp-test         # Test MCP currency exchange tool
./run.sh a2a              # Start A2A agent server (:10000)
./run.sh a2a-test         # Run A2A client test
./run.sh a2ui-backend     # Start A2UI v0.9 agent (:10001)
./run.sh a2ui-frontend    # Launch Lit Web Client (:5173)
./run.sh agui-backend     # Start AG-UI FastAPI server (:8000)
./run.sh agui-frontend    # Launch Next.js Copilot UI (:3000)
```

---

## 📚 Workshop Slides

The lecture and architectural presentation slides are available in:
👉 [`slides/Agentic Systems - Patterns - Protocols.pdf`](./slides/Agentic%20Systems%20-%20Patterns%20-%20Protocols.pdf)

See [`slides/readme.md`](./slides/readme.md) for session outline and discussion points.

---

## 🔑 Key Engineering Standards

- **Model Standardization**: Standardized across all patterns and protocols on **Gemini 3.5 Flash** with dynamic override support (`GEMINI_MODEL`).
- **Modern Package Management**: Zero-friction setup using `uv` with deterministic lockfiles (`uv.lock`).
- **Clean Architecture & SOLID**: Centralized shared utilities, single-responsibility components, and comprehensive test coverage.
- **Protocol Conformity**: Implements the official specifications for MCP, A2A, A2UI v0.9, and AG-UI.