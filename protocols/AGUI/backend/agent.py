import logging
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

load_dotenv()

SYSTEM_INSTRUCTION = """
You are a helpful assistant that provides currency information.
To answer questions about exchange rates, use the 'get_exchange_rate' tool.

When providing information, be concise and friendly.
"""

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

root_agent = LlmAgent(
    model=MODEL_NAME,
    name="agui_currency_agent",
    description="An agent compatible with AG-UI protocol for currency exchange",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")
            )
        )
    ],
)
