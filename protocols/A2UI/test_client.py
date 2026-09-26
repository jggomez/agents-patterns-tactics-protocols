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
    print("\n--- 📱 A2UI v0.9 RENDERER (Adjacency List) ---")
    data_models = {}

    for msg in messages:
        version = msg.get("version", "legacy")
        
        # 1. createSurface
        if "createSurface" in msg:
            cs = msg["createSurface"]
            surface_id = cs.get("surfaceId", "default")
            catalog_id = cs.get("catalogId", "basic")
            print(f"🔹 [createSurface] surfaceId='{surface_id}' (version: {version})")
            print(f"   Catalog: {catalog_id}")

        # 2. updateDataModel
        if "updateDataModel" in msg:
            udm = msg["updateDataModel"]
            surface_id = udm.get("surfaceId", "default")
            path = udm.get("path", "/")
            val = udm.get("value", {})
            data_models[surface_id] = val
            print(f"📊 [updateDataModel] surfaceId='{surface_id}' path='{path}': {val}")

        # 3. updateComponents (v0.9) or surfaceUpdate (legacy)
        components_list = None
        surface_id = "default"

        if "updateComponents" in msg:
            uc = msg["updateComponents"]
            surface_id = uc.get("surfaceId", "default")
            components_list = uc.get("components", [])
            print(f"🧩 [updateComponents] surfaceId='{surface_id}' ({len(components_list)} components):")
        elif "surfaceUpdate" in msg:
            su = msg["surfaceUpdate"]
            surface_id = su.get("surfaceId", "default")
            components_list = su.get("components", [])
            print(f"🧩 [surfaceUpdate (legacy)] surfaceId='{surface_id}' ({len(components_list)} components):")

        if components_list:
            comp_map = {c["id"]: c for c in components_list if "id" in c}
            if "root" in comp_map:
                render_component(comp_map["root"], comp_map, indent=1)
            else:
                print("   ⚠️ No 'root' component found in component list.")

    print("---------------------------------------------\n")

def render_component(comp, all_components, indent=1):
    space = "  " * indent
    comp_type = comp.get("component", "Unknown")
    comp_id = comp.get("id", "?")
    props = comp.get("properties") or comp.get("props") or comp
    
    # Header info
    info = []
    if comp_type == "Text":
        text_val = props.get("text", "")
        variant = props.get("variant") or props.get("usageHint", "body")
        info.append(f'text="{text_val}" [{variant}]')
    elif comp_type == "Button":
        variant = props.get("variant", "default")
        label = props.get("label", "")
        action = props.get("action", "")
        action_name = action.get("name", str(action)) if isinstance(action, dict) else str(action)
        if label:
            info.append(f'label="{label}"')
        info.append(f'[{variant}] action="{action_name}"')
    elif comp_type == "Card":
        info.append("[Container]")

    info_str = " " + " ".join(info) if info else ""
    print(f"{space}[{comp_type}] id={comp_id}{info_str}")
    
    # Render child (Card, Button) or children (Column, Row)
    children_ids = list(props.get("children", []))
    single_child = props.get("child")
    if single_child:
        children_ids.append(single_child)

    for child_id in children_ids:
        if child_id in all_components:
            render_component(all_components[child_id], all_components, indent + 1)
        else:
            print(f"{space}  ⚠️ Child ID '{child_id}' not found!")

if __name__ == "__main__":
    asyncio.run(main())
