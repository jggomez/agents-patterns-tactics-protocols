# AI Agent Workflow Patterns with Google ADK

This directory explores classic agent workflow patterns implemented using the **Google Agent Development Kit (ADK)**. These patterns demonstrate different ways to coordinate multiple agents or structure complex workflows.

## 📂 Structure

The patterns are located in the `agents/` directory, each demonstrating a specific orchestration strategy:

```
patterns/
└── agents/
    ├── first_agent/         # Basic conversational agent with tool integration
    ├── loop_agent/          # Iterative refinement with feedback loops
    ├── orchestrator_agent/  # Dynamic coordination using the Agent-as-Tool pattern
    ├── parallel_agent/      # Concurrent execution for multi-faceted tasks
    └── sequential_agent/    # Linear pipelines for multi-stage workflows
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

---

## 🔑 Key Concepts Covered

- **Agent Orchestration**: Coordinating multiple specialized models to solve complex tasks.
- **Tool Integration**: Connecting LLMs to external data sources (Google Search, APIs) via `FunctionTool`.
- **State Management**: Passing context between agents using `output_key` and session state.
- **Declarative Instructions**: Using structured system prompts to define roles and autonomy.

## 🤖 Agent Instructions Template (SOP)

When building your own agents, use this template to ensure consistent behavior:

#### 1. IDENTITY & ROLE
You are **{{Agent Name}}**, an AI specialized in **{{Domain}}**.
Your primary objective is: **{{Primary Objective}}**.

#### 2. OPERATIONAL MODE
- **STRICT GUIDELINES**: Follow the SOP exactly. Do not deviate.
- **STRATEGIC PLANNING**: Plan first, self-correct, and proactively find missing information.

#### 3. TOOLS & CAPABILITIES
You have access to:
- `{{tool_name}}`: {{Precise description of intent and returns}}.

#### 4. REASONING PROTOCOL (ReAct)
Before responding, use an internal monologue to think through the steps:
`Thought -> Action -> Observation -> Final Answer`

---

## 🛠️ Prerequisites

- **Python 3.10+**
- **Google API Key** (Gemini)
- **Environment variables** configured in a `.env` file.

> [!TIP]
> Each agent directory contains its own `agent.py` and `commons.py` explaining the specific implementation details of that pattern.
