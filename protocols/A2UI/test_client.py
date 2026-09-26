import asyncio
import httpx
import json
from uuid import uuid4
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import SendMessageRequest, MessageSendParams

AGENT_URL = "http://localhost:10001"

async def main():
    print(f"--- 🔄 Connecting to A2UI agent at {AGENT_URL}... ---")
    async with httpx.AsyncClient(timeout=60.0) as httpx_client:
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=AGENT_URL)
        agent_card = await resolver.get_agent_card()
        client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)
        
        print("--- ✅ Connection successful. ---")
        
        # Request
        text = "Show me the exchange rate for 100 USD to MXN"
        payload = {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": text}],
                "messageId": uuid4().hex,
            },
        }
        request = SendMessageRequest(id=str(uuid4()), params=MessageSendParams(**payload))
        
        print(f"--- ✉️  Sending Message: '{text}' ---")
        response = await client.send_message(request)
        
        print("--- 📥 Response Received ---")
        
        if hasattr(response.root, 'result'):
            history = response.root.result.history
            for turn in history:
                if turn.role == "agent":
                    for part in turn.parts:
                        actual_part = part.root
                        
                        if hasattr(actual_part, 'text') and actual_part.text:
                            content = actual_part.text
                            if "---a2ui_JSON---" in content:
                                parts = content.split("---a2ui_JSON---")
                                text_response = parts[0].strip()
                                json_response = parts[1].strip()
                                
                                if text_response:
                                    print(f"Agent Text: {text_response}")
                                
                                try:
                                    # Handle cases where LLM might wrap JSON in backticks
                                    if json_response.startswith("```json"):
                                        json_response = json_response.replace("```json", "", 1).replace("```", "", 1).strip()
                                    elif json_response.startswith("```"):
                                        json_response = json_response.replace("```", "", 1).replace("```", "", 1).strip()
                                        
                                    ui_messages = json.loads(json_response)
                                    render_a2ui(ui_messages)
                                except Exception as e:
                                    print(f"--- ⚠️ Error parsing A2UI JSON: {e} ---")
                                    print(f"Raw JSON was: {json_response}")
                            else:
                                print(f"Agent Text: {content}")

def render_a2ui(messages: list):
    print("\n--- 📱 A2UI RENDERER (Adjacency List) ---")
    for msg in messages:
        if "surfaceUpdate" in msg:
            update = msg["surfaceUpdate"]
            components = {c["id"]: c for c in update["components"]}
            
            # Start rendering from root
            if "root" in components:
                render_component(components["root"], components, indent=0)
            else:
                print("⚠️ No 'root' component found in surfaceUpdate.")
    print("----------------------------------------\n")

def render_component(comp, all_components, indent=0):
    space = "  " * indent
    comp_type = comp.get("component", "Unknown")
    comp_id = comp.get("id", "?")
    props = comp.get("props", {})
    
    # Header for the component
    info = ""
    if comp_type == "Text":
        info = f'"{props.get("text", "")}"'
    elif comp_type == "Button":
        info = f'label="{props.get("label", "")}"'
    
    print(f"{space}[{comp_type}] id={comp_id} {info}")
    
    # Render children
    children_ids = comp.get("children", [])
    for child_id in children_ids:
        if child_id in all_components:
            render_component(all_components[child_id], all_components, indent + 1)
        else:
            print(f"{space}  ⚠️ Child ID '{child_id}' not found!")

if __name__ == "__main__":
    asyncio.run(main())
