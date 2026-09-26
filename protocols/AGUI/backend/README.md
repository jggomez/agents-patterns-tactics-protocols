# AG-UI Backend (Google ADK + FastAPI)

This directory implements the backend service for the **AG-UI (Agent-User Interaction)** protocol using **Google ADK** and **FastAPI**. It transforms an ADK agent into a streaming copilot service compatible with CopilotKit frontends.

---

## 🏗️ Architecture

- **`agent.py`**: Configures the `LlmAgent` with **Gemini 3.5 Flash** (via `GEMINI_MODEL`), instruction sets, and connects to the FastMCP toolset for currency exchange rates (`get_exchange_rate`).
- **`main.py`**: Wraps the ADK agent using `ag-ui-adk`'s `ADKAgent` adapter and serves the AG-UI event stream over FastAPI on port `8000`.
- **`pyproject.toml`**: Declares dependencies (`ag-ui-adk`, `google-adk`, `fastapi`, `uvicorn`, `fastmcp`) with Python `>=3.10`.
- **`.env.example`**: Environment template supporting `GEMINI_API_KEY`, `GEMINI_MODEL`, `PORT`, and `MCP_SERVER_URL`.

---

## 🚀 Setup & Execution

### 1. Environment Configuration
```bash
# Copy template
cp .env.example .env
# Edit .env and configure GEMINI_API_KEY
```

### 2. Install Dependencies
```bash
uv sync
```

### 3. Run the Backend Server
```bash
uv run python main.py
# Or from protocols root:
./run.sh agui-backend
```

The AG-UI endpoint will listen on `http://localhost:8000/`.
