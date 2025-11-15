from google.adk.agents import LlmAgent, LoopAgent
from google.adk.tools import google_search
from .util import load_instruction_from_file


SMA = LlmAgent(
    name = "StockMarketAgent",
    model = "gemini-2.0-flash-001",
    instruction = load_instruction_from_file("sma_instruction.txt", 
    default_instruction="You are a helpful stock market analysis agent."),
    tools = [google_search],
    output_key = "SMA_output"
)

BS = LlmAgent(
    name = "BadStocksAgent",
    model = "gemini-2.0-flash-001",
    instruction = load_instruction_from_file("bs_instruction.txt",
    default_instruction="You are a helpful bad stocks identification agent."),
    tools = [google_search],
    output_key = "BS_output"
)

GS = LlmAgent(
    name = "GoodStocksAgent",
    model = "gemini-2.0-flash-001",
    instruction = load_instruction_from_file("gs_instruction.txt",
    default_instruction="You are a helpful good stocks identification agent."),
    tools = [google_search],
    output_key = "GS_output"
)


stock_market_agents = LoopAgent(
     name="stock_market_agents",
    max_iterations=3,
    sub_agents=[SMA, BS, GS],
)
root_agent = stock_market_agents

from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner


# Load .env
# Replace the API_KEY in .env file.
from dotenv import load_dotenv

load_dotenv()

# Instantiate constants
APP_NAME = "stock_markets_app"
USER_ID = "12345"
SESSION_ID = "123344"

# Session and Runner
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=stock_market_agents, app_name=APP_NAME, session_service=session_service)
    return session, runner


# Agent Interaction
async def call_agent_async(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)

call_agent_async("Tell me about the current stock market trends and identify some good and bad stocks.")