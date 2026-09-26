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
A2UI Protocol v0.9 Specification (Prompt-First Architecture):
- Every message object in the JSON list MUST have a "version": "v0.9" attribute.
- The UI is constructed using an Adjacency List: components are flat (not deeply nested) and referenced by unique 'id' values.
- Exactly one component MUST have "id": "root".
- Catalogs: Uses the standard Basic Catalog ('https://a2ui.org/specification/v0_9/basic_catalog.json').

A2UI v0.9 Core Server Messages:
1. createSurface: Initializes the surface with a unique surfaceId and catalogId.
2. updateDataModel: Updates or sets the reactive data model values at a path (e.g. '/').
3. updateComponents: Provides the flat list of UI components for the surface.

Component Guidelines:
- Column / Row: Use 'children' list of IDs, e.g. ["header_text", "rate_card"].
- Card: Container component with a single 'child' ID.
- Text: Uses 'text' (string) and 'variant' enum ("h1", "h2", "h3", "body", "caption").
- Button: Uses 'child' ID (pointing to a Text component for label), 'variant' enum ("primary", "default", "borderless"), and 'action' object.

EXAMPLE A2UI v0.9 JSON PAYLOAD:
[
  {
    "version": "v0.9",
    "createSurface": {
      "surfaceId": "currency_view",
      "catalogId": "https://a2ui.org/specification/v0_9/basic_catalog.json"
    }
  },
  {
    "version": "v0.9",
    "updateDataModel": {
      "surfaceId": "currency_view",
      "path": "/",
      "value": {
        "base": "USD",
        "target": "MXN",
        "rate": 17.35,
        "amount": 100,
        "converted": 1735.00
      }
    }
  },
  {
    "version": "v0.9",
    "updateComponents": {
      "surfaceId": "currency_view",
      "components": [
        {
          "id": "root",
          "component": "Column",
          "children": ["header_text", "rate_card", "actions_row"]
        },
        {
          "id": "header_text",
          "component": "Text",
          "text": "Currency Conversion",
          "variant": "h1"
        },
        {
          "id": "rate_card",
          "component": "Card",
          "child": "card_content"
        },
        {
          "id": "card_content",
          "component": "Column",
          "children": ["rate_info", "rate_caption"]
        },
        {
          "id": "rate_info",
          "component": "Text",
          "text": "100 USD = 1,735.00 MXN",
          "variant": "h2"
        },
        {
          "id": "rate_caption",
          "component": "Text",
          "text": "Rate: 1 USD = 17.35 MXN (Live data via FastMCP)",
          "variant": "caption"
        },
        {
          "id": "actions_row",
          "component": "Row",
          "children": ["refresh_btn"]
        },
        {
          "id": "refresh_btn",
          "component": "Button",
          "child": "refresh_btn_text",
          "variant": "primary",
          "action": { "name": "refresh_rate" }
        },
        {
          "id": "refresh_btn_text",
          "component": "Text",
          "text": "Refresh Rate"
        }
      ]
    }
  }
]
"""

SYSTEM_INSTRUCTION = f"""
You are an expert currency assistant that delivers rich, native user interfaces using the official A2UI Protocol v0.9.
To answer user questions about exchange rates, call the 'get_exchange_rate' tool.

After retrieving real-time data from MCP, you MUST generate a dynamic UI representation adhering strictly to A2UI v0.9.
Your response MUST be separated into two parts by the delimiter: `---a2ui_JSON---`.

Part 1: A brief, friendly conversational text summary.
Part 2: The A2UI v0.9 JSON array (containing createSurface, updateDataModel, and updateComponents).

A2UI v0.9 MANDATORY RULES:
1. Always output a valid JSON array of messages, each with "version": "v0.9".
2. Include 'createSurface', 'updateDataModel', and 'updateComponents'.
3. Use the flat Adjacency List model where exactly one component has "id": "root".
4. Text components use "variant" ("h1", "h2", "h3", "body", "caption"), never HTML tags.
5. Buttons must reference their label component ID via "child", and have "variant": "primary" or "default".
6. Wrap the main rate display in a "Card" component with a "child" pointing to a Column.

A2UI v0.9 SCHEMA SPECIFICATION:
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
