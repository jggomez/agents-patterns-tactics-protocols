from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner


async def get_runner(root_agent):
    session_service = InMemorySessionService()

    APP_NAME = "example-parallel"
    USER_ID = "user_1"
    SESSION_ID = "session_001"

    # Create the specific session where the conversation will happen
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    print(
        f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}')")

    # ---Runner ---
    # Key Concept: Runner orchestrates the agent execution loop.
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    print(f"Runner created for agent '{runner.agent.name}'.")
    return runner, USER_ID, SESSION_ID


async def call_agent_async(query: str, runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""

    print(f"\n>>> User Query: {query}")

    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response."

    # We iterate through events to find the final answer.
    # Don't break early - consume all events to properly close the async generator
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):

        # Key Concept: is_final_response() marks the concluding message for the turn.
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:  # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            # Continue to consume remaining events instead of breaking
            break

    print(f"<<< Agent Response: {final_response_text}")
    return final_response_text
