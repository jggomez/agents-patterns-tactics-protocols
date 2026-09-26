# Workshop Slides: Agentic Systems - Patterns & Protocols

This directory contains the presentation slides accompanying the hands-on workshop:

👉 [**`Agentic Systems - Patterns - Protocols.pdf`**](./Agentic%20Systems%20-%20Patterns%20-%20Protocols.pdf)

---

## 📑 Agenda & Key Topics Covered

1. **Evolution of Autonomous Agents**:
   - From simple LLM prompting to autonomous multi-agent systems.
   - Core architecture: Perception, Memory, Planning, and Action execution.

2. **Google Agent Development Kit (ADK)**:
   - Concepts: `LlmAgent`, `FunctionTool`, session runtimes, and context models.
   - Standardizing on **Gemini 3.5 Flash** for high reasoning throughput and cost efficiency.

3. **Agent Orchestration Patterns**:
   - Simple Agent (single-task + function calling).
   - Sequential Pipelines (linear state passing).
   - Parallel Fan-Out (concurrent specialist execution).
   - Dynamic Orchestrator (Agent-as-Tool with `AgentTool`).
   - Iterative Loops (self-correcting feedback cycles).
   - Graph Workflows (native **ADK 2.0** DAGs with deterministic nodes, routing, fan-out, and barrier joins).

4. **Agent Interoperability Protocols**:
   - **MCP (Model Context Protocol)**: Universal data/tool connectivity over HTTP SSE.
   - **A2A (Agent-to-Agent)**: Service discovery with `AgentCard` and JSON-RPC task interchange.
   - **A2UI (Agent-to-User Interface v0.9)**: Declarative, Prompt-First UI streaming with Web Components (Lit) and `@a2ui/web_core`.
   - **AG-UI**: Event streaming bridge to modern React/Next.js copilot experiences (CopilotKit).
