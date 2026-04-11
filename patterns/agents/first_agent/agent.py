import asyncio
from google.genai import types
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from Patterns.agents.first_agent.commons import call_agent_async
from Patterns.agents.first_agent.commons import get_runner
from dotenv import load_dotenv

load_dotenv()

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)


async def run_conversation():
    runner, user_id, session_id = await get_runner(root_agent)
    await call_agent_async("What is the weather like in CDMX", runner, user_id, session_id)
    await call_agent_async("How about Monterrey?", runner, user_id, session_id)
    await call_agent_async("Tell me the weather in Puebla", runner, user_id, session_id)


def main():
    asyncio.run(run_conversation())


if __name__ == "__main__":
    main()
