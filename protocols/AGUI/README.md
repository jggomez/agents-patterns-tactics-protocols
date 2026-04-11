# AG-UI (Agent-User Interaction) - CopilotKit Integration

This directory contains a full-stack example of the **AG-UI** protocol, designed to bridge AI agents with modern web frontends using **CopilotKit**.

## 🚀 AG-UI: Standardizing Agent Frontends

AG-UI is an open, lightweight, event-based protocol that standardizes how agent backends connect to agent frontends. In this example, we use the `ag-ui-adk` package to transform a standard Google ADK agent into an AG-UI compatible service.

### Key Benefits:
- **Interoperability**: Connect the same ADK agent to different frontends (React, Next.js, etc.).
- **Rich Interaction**: Leverages CopilotKit's pre-built UI components (Chat Sidebar, Popups).
- **Tool Transparency**: Tool calls and agent status are communicated via a standardized event stream.

## 🛠️ System Architecture

1.  **MCP Server** (`../MCP/server.py`): The data source for currency exchange rates.
2.  **AG-UI Backend** (`backend/main.py`):
    - Powered by **FastAPI**.
    - Wraps the ADK agent with `ADKAgent` middleware.
    - Exposes the AG-UI endpoint at `/`.
3.  **Next.js Frontend** (`frontend/`):
    - Uses `@copilotkit/react-core` and `@copilotkit/react-ui`.
    - Features a "Currency Assistant" popup.
    - Communicates with the backend via the `/api/copilotkit` runtime adapter.

## 🏁 How to Run

### 1. Start the MCP Server
```bash
cd ../MCP
uv run python server.py
```

### 2. Start the AG-UI Backend
```bash
cd backend
uv run python main.py
```

### 3. Start the Next.js Frontend
```bash
cd frontend
source ~/.nvm/nvm.sh
npm run dev
```

### 4. Interact
Open `http://localhost:3000` and ask the floating "Currency Assistant" (bottom right):
> *"How much is 100 USD in MXN?"*

## 📝 Configuration Note

If you change the agent name in `backend/main.py`, ensure you update both the `src/app/api/copilotkit/route.ts` (agent mapping) and the `agent` prop in the `CopilotKit` provider in `src/app/layout.tsx`.
