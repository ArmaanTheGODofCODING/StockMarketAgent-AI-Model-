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
    model = "gemini-2.5-flash-001",
    instruction = load_instruction_from_file("bs_instruction.txt",
    default_instruction="You are a helpful bad stocks identification agent."),
    tools = [google_search],
    output_key = "BS_output"
)

GS = LlmAgent(
    name = "GoodStocksAgent",
    model = "gemini-2.5-flash-001",
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
