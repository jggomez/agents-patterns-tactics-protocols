import logging
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

load_dotenv()



A2UI_SCHEMA_EXPLANATION = """
A2UI uses a flat 'Adjacency List' model for UI. 
- Components are not nested. Every component has an 'id'.
- Parent components reference children by their 'id' in a 'children' list property.
- The UI is sent as a list of independent components in a 'surfaceUpdate' message.

EXAMPLE A2UI JSON:
[
  {
    "surfaceUpdate": {
      "surfaceId": "currency_view",
      "components": [
        {
          "id": "root",
          "component": "Column",
          "children": ["header_text", "rate_info", "refresh_btn"]
        },
        {
          "id": "header_text",
          "component": "Text",
          "props": { "text": "Currency Conversion", "usageHint": "h1" }
        },
        {
          "id": "rate_info",
          "component": "Text",
          "props": { "text": "1 USD = 17.35 MXN", "usageHint": "body" }
        },
        {
          "id": "refresh_btn",
          "component": "Button",
          "props": { "label": "Refresh", "action": "refresh_rate" }
        }
      ]
    }
  }
]
"""

SYSTEM_INSTRUCTION = f"""
You are a helpful assistant that provides currency information.
To answer questions about exchange rates, use the 'get_exchange_rate' tool.

After you get the data, you MUST generate a dynamic UI representation using the A2UI protocol.
Your response MUST be separated into two parts by the delimiter: `---a2ui_JSON---`.

Part 1: A brief conversational text response.
Part 2: The A2UI JSON block (a list of messages).

A2UI PROTOCOL RULES:
- Use the 'Adjacency List' model (flat structure, components linked by IDs).
- The root component ID should always be 'root'.
- Use components: Column, Row, Text, Button, Image.
- DO NOT use HTML tags in strings. Use 'usageHint' for styling (h1, h2, body, caption).
- Data binding: You can use paths in props if needed, but for this example, literal values are fine.

A2UI SCHEMA GUIDE:
{A2UI_SCHEMA_EXPLANATION}
"""

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

root_agent = LlmAgent(
    model=MODEL_NAME,
    name="ui_currency_agent",
    description="An agent that returns dynamic A2UI components",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")
            )
        )
    ],
)

# Expose as A2A
port = int(os.getenv("PORT", 10001))
a2a_app = to_a2a(root_agent, port=port)

# Add CORS
a2a_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting A2UI Agent Server on port {port} (model: {MODEL_NAME})...")
    uvicorn.run(a2a_app, host="0.0.0.0", port=port)
