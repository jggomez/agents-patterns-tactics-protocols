# MCP (Model Context Protocol) Server Example

This directory contains a practical implementation of a **Model Context Protocol (MCP)** server using **FastMCP**.

## 🚀 Introduction to MCP

The **Model Context Protocol (MCP)** is an open-standard used to connect AI models (LLMs) to data and tools. It provides a standardized interface for:
- **Tool Discovery**: Allowing agents to automatically find available tools.
- **Resource Management**: Exposing data or logs as resources that models can read.
- **Interoperability**: Ensuring that tools built for one agent framework can easily be used by another (like the A2A agent).

In this example, we use the **FastMCP** framework to quickly expose high-level tools via an HTTP/SSE transport.

## 🛠️ Implementing and Exposing Tools with FastMCP

FastMCP simplifies the creation of MCP servers by providing decorator-based tool definitions.

### Implemented Tool: `get_exchange_rate`
This tool fetches current exchange rates from the Frankfurter API. It is defined in `server.py` using the `@mcp.tool()` decorator:

```python
@mcp.tool()
def get_exchange_rate(currency_from: str = "USD", currency_to: str = "EUR", currency_date: str = "latest"):
    # Fetches real-time rate from Frankfurter API
    ...
```

## 📂 Project Structure

- **[server.py](server.py)**: The core MCP server. It listens on port 8080 and exposes the `get_exchange_rate` tool via a Streamable-HTTP interface at `/mcp`.
- **[test_server.py](test_server.py)**: A client script that connects to the local server, lists available tools, and executes a test call to verify everything is working.
- **[pyproject.toml](pyproject.toml)**: Defines the Python environment and dependencies (`fastmcp`, `httpx`).

## 🛠️ Installation

This project uses `uv` for dependency management.

```bash
# Install dependencies into a local virtual environment
uv sync
```

## 🏁 Execution and Testing

Follow these steps to run the server and verify it:

### 1. Run the MCP Server
Start the server in your terminal. It will default to port 8080.

```bash
uv run server.py
```

### 2. Test the Server
In a separate terminal, run the test script to ensure the tools are reachable.

```bash
uv run test_server.py
```

> [!TIP]
> This server uses the `http` transport. The primary endpoint for clients (like our A2A Agent) is:
> 👉 [http://localhost:8080/mcp](http://localhost:8080/mcp)
