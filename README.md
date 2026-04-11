# Workshop: AI Agent Patterns & Interoperability Protocols

A comprehensive hands-on workshop exploring the design, orchestration, and standardization of AI Agents. This repository demonstrates how to build modular, autonomous systems using the **Google Agent Development Kit (ADK)** and the latest industry protocols.

## 📂 Project Structure

The workshop is organized into two primary pillars:

### 1. [Agent Patterns](./patterns)
Classic workflow patterns for structuring agentic logic and multi-agent coordination.
- **Sequential**: Linear pipelines (Outline -> Write -> Edit).
- **Parallel**: Concurrent task execution for speed and modularity.
- **Orchestrator**: Dynamic coordination using the "Agent-as-Tool" pattern.
- **Loop**: Iterative refinement and self-correction cycles.

### 2. [Standard Protocols](./protocols)
Implementation of industry-standard interoperability protocols for agents.
- **[MCP (Model Context Protocol)](./protocols/MCP)**: Exposing local tools and data sources to any AI system.
- **[A2A (Agent-to-Agent)](./protocols/A2A)**: Standardized communication between independent agent services.
- **[A2UI (Agent-to-User Interface)](./protocols/A2UI)**: Declarative UI generation using modern web components (Lit).
- **[AG-UI (Agent-User Interaction)](./protocols/AGUI)**: Event-based bridge to React/Next.js frontends via CopilotKit.

---

## 🎯 Learning Objectives

- **Orchestration**: Understand when to use sequential, parallel, or dynamic (orchestrator) patterns.
- **Interoperability**: Connect multi-vendor agents and frontends using standardized protocols.
- **Tooling**: Build and integrate custom tools using `FunctionTool` and MCP.
- **UI Design**: Learn how agents can "own" the user interface through declarative UI patterns.
- **Scale**: Design systems that scale from simple chat-bots to complex multi-agent ecosystems.

## 🚀 Getting Started

Each directory contains a specialized `README.md` with specific setup instructions.

1.  **Environment**: Create a `.env` file in the root with your `GOOGLE_API_KEY`.
2.  **Prerequisites**:
    - **Python 3.10+** (using `uv` or `poetry`).
    - **Node.js 20+** (for UI components).
3.  **Exploration**:
    - Start with [Patterns](./patterns) to understand agent logic.
    - Move to [Protocols](./protocols) to learn about standardizing connections.

---

## 🛠️ Key Technologies

- **Framework**: [Google ADK](https://github.com/google/adk)
- **Protocol Reference**: MCP, AG-UI (CopilotKit)
- **Frontend**: Next.js, Lit Web Components, Tailwind CSS
- **Models**: Gemini 2.0/2.5 Flash

---

*This workshop is designed to provide a deep dive into the engineering of modern, interoperable AI agents.*