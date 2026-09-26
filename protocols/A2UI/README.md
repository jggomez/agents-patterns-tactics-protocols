# A2UI (Agent-to-User Interface) - Official Adjacency List Protocol

This directory contains a modern, production-grade example of the **Agent-to-User Interface (A2UI)** protocol within an A2A (Agent-to-Agent) ecosystem.

## 🚀 The A2UI Evolution: Adjacency List Model

In this implementation, the A2UI protocol uses the **Adjacency List** model. Unlike traditional deeply nested JSON trees, this model represents UI components as a flat list where parents reference children by their unique IDs.

### Why Adjacency Lists?
- **LLM-Friendly**: Models generate flat structures more reliably than complex nested hierarchies.
- **Streaming Support**: Clients can render components as they arrive in the stream.
- **Incremental Updates**: Update single components without re-sending the entire UI state.

## 🛠️ System Architecture

1.  **MCP Server** (`../MCP/server.py`): Provides real-time exchange rate data.
2.  **AI Agent** (`agent.py`): 
    - Fetches data via MCP.
    - Generates a dynamic UI using the A2UI Adjacency List schema.
    - Delivers the UI payload via A2A with the `---a2ui_JSON---` delimiter.
    - **CORS Enabled** to allow web client communication.
3.  **Lit Web Client** (`client-lit/`):
    - Built with **Lit (Web Components)** and **TypeScript**.
    - Implements a pure A2UI Message Processor and Renderer.
    - Native components: `a2ui-text`, `a2ui-button`, `a2ui-column`, `a2ui-row`.

## 📂 Project Structure

- **`agent.py`**: The A2UI Agent server (Port 10001).
- **`client-lit/`**: Modern web client (Port 5173).
- **`test_client.py`**: Python-based CLI simulator.

## 🏁 How to Run

### 1. Start the MCP Server
```bash
cd ../MCP
uv run python server.py
```

### 2. Start the A2UI Agent
```bash
# Return to A2UI directory if you were in MCP
cd ../A2UI 
uv run python -m uvicorn agent:a2a_app --host localhost --port 10001
# OR
uv run python agent.py
```

### 3. Launch the Lit Web Client
```bash
cd client-lit
source ~/.nvm/nvm.sh  # If using NVM
npm install
npm run dev
```

### 4. Open the UI
Go to `http://localhost:5173` (or the port shown by Vite) and ask:
> *"What is the exchange rate for 100 USD to MXN?"*

## 📝 A2UI Protocol Detail (JSONRPC)

The web client communicates using the following JSON-RPC structure:

- **Method**: `message/send`
- **Params**:
  ```json
  {
    "message": {
      "role": "user",
      "parts": [{"kind": "text", "text": "YOUR MESSAGE"}],
      "messageId": "UNIQUE_ID"
    }
  }
  ```

The agent responds with a `Task` object containing the `history`. The client then parses the `---a2ui_JSON---` block from the last agent turn and passes the `components` list to the `<a2ui-surface>` renderer.
