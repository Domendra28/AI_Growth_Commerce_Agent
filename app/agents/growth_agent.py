from typing import List, Any
from google.adk import Agent
from app.tools.growth_tools import analyze_upsell_tool, analyze_cross_sell_tool, orchestrate_campaign_tool
from app.config import config

GROWTH_INSTRUCTION = """
You are the AI Growth Agent.
Your role is to help merchants increase revenue, optimize Average Order Value (AOV), and provide personalized cross-sell and upsell recommendations to buyers.

Guidelines:
1. Explainable Upselling: Explain why upgrading to a higher tier product provides value relative to price difference.
2. Cross-Selling: Recommend complementary accessories that pair naturally with the chosen item.
3. Campaign Orchestration: Help merchants generate targeted campaigns with expected ROI impact, enforcing explicit merchant authorization before activation.
"""

class GrowthAgent(Agent):
    name: str = "growth_agent"
    description: str = "Handles revenue growth analysis, AI upselling, cross-selling recommendations, and merchant campaign orchestration."
    instruction: str = GROWTH_INSTRUCTION
    tools: List[Any] = [analyze_upsell_tool, analyze_cross_sell_tool, orchestrate_campaign_tool]

def create_growth_agent() -> GrowthAgent:
    return GrowthAgent(
        model=config.google_genai_model,
        instruction=GROWTH_INSTRUCTION,
        tools=[analyze_upsell_tool, analyze_cross_sell_tool, orchestrate_campaign_tool]
    )
