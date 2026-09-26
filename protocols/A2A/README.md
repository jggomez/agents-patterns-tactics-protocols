# A2A (Agent-to-Agent) Protocol Example

This directory contains a practical example of how to implement the **Agent-to-Agent (A2A)** protocol using the **Google Agent Development Kit (ADK)** and the **A2A SDK**.

## 🚀 Introduction to A2A

The **A2A protocol** is designed to enable seamless, standardized communication between different AI agents. It provides a structured way for agents to:
- Discover each other's capabilities via the **AgentCard**.
- Exchange messages and tasks using a consistent JSON-RPC over HTTP transport.
- Manage multi-turn conversations and task states (streaming, non-streaming, artifacts, etc.).

In this example, we have a specialized `currency_agent` that can perform currency exchanges by connecting to an external **MCP (Model Context Protocol)** server.

## 🤖 how to Expose your Agents with A2A using ADK

Exposing an existing ADK agent to the A2A protocol is straightforward thanks to the `to_a2a` utility. 

1. Create your `LlmAgent` as usual.
2. Wrap it using `to_a2a(root_agent, port=10000)`.
3. The resulting `a2a_app` is a FastAPI-based server that exposes:
    - **Handshake/Discovery**: `GET http://localhost:10000/.well-known/agent.json` (The AgentCard).
    - **Messaging**: The JSON-RPC endpoint for A2A communication.

### Visualize your AgentCard
Once the server is running, you can view the agent's definition and capabilities by visiting:
👉 [http://localhost:10000/.well-known/agent.json](http://localhost:10000/.well-known/agent.json)

## 📂 Project Structure

- **[agent.py](agent.py)**: The core agent definition. It configures the `LlmAgent` with Vertex AI, sets up the system instructions, and connects to the MCP toolset for currency exchange rates. It then wraps the agent for A2A exposure.
- **[test_client.py](test_client.py)**: A standalone test client using the `a2a-sdk`. It simulates an external caller by resolving the AgentCard, sending a message, and querying the resulting task state.
- **[.env](.env)**: Contains environment variables for Vertex AI configuration (`PROJECT_ID`, `LOCATION`, etc.).
- **[pyproject.toml](pyproject.toml)**: Defines the Python environment and dependencies (`google-adk`, `a2a-sdk`, `fastmcp`).

## 🛠️ Installation

This project uses `uv` for lightning-fast dependency management.

```bash
# Install dependencies and create a virtual environment
uv sync
```

## 🏁 Execution Workflow

To see the A2A protocol in action, follow these steps in order:

### 1. Start the MCP Server
Ensure you have the MCP server running (usually on port 8080). This server provides the actual `get_exchange_rate` tool logic.

### 2. Start the A2A Agent Server
Run the agent server using `uvicorn`. This command will detect the `a2a_app` and start listening on port 10000.

```bash
# Recommended: Run using uvicorn directly
uv run python -m uvicorn agent:a2a_app --host localhost --port 10000

# Alternative: Run the script directly
uv run python agent.py
```

### 3. Run the Test Client
Once the agent server is up, execute the test client to send a currency conversion request.

```bash
uv run test_client.py
```

> [!IMPORTANT]
> Since LLM and tool calls can be slow, the `test_client.py` is configured with a 60-second timeout to prevent premature connection drops.
