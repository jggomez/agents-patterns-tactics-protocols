import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from agent import root_agent
from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Create ADK middleware agent instance
adk_agent = ADKAgent(
    adk_agent=root_agent,
    app_name="currency_exchange_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)

# Create FastAPI app
app = FastAPI(title="AG-UI Exchange Rate Agent")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the ADK endpoint at root
add_adk_fastapi_endpoint(app, adk_agent, path="/")

@app.get("/info")
async def get_info():
    """Expose agent capabilities and tools."""
    tools = []
    # Extract tools from root_agent
    if hasattr(root_agent, 'tools'):
        for toolset in root_agent.tools:
            # MCPToolset or other toolsets
            if hasattr(toolset, 'get_tools'):
                # Handle possible async get_tools
                import asyncio
                if asyncio.iscoroutinefunction(toolset.get_tools):
                    available_tools = await toolset.get_tools()
                else:
                    available_tools = toolset.get_tools()
                
                for t in available_tools:
                    tools.append({
                        "name": t.name,
                        "description": t.description
                    })
    
    return {
        "name": root_agent.name,
        "description": root_agent.description,
        "instruction": root_agent.instruction,
        "tools": tools
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting AG-UI Agent with Info endpoint on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
