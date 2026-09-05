from typing import List, Any
from google.adk import Agent
from app.agents.shopping_agent import create_shopping_agent, ShoppingAgent
from app.agents.growth_agent import create_growth_agent, GrowthAgent
from app.agents.payment_agent import create_payment_agent, PaymentAgent
from app.config import config

ROOT_INSTRUCTION = """
You are the Root AI Growth & Agentic Commerce Orchestrator.
Your goal is to assist merchants with AI Growth (upselling, cross-selling, campaign strategies) and empower AI buyers to execute complete, safe, end-to-end commerce transactions over UCP and AP2 protocols.

Delegation Strategy:
- Delegate product discovery, catalog browsing, cart creation, and checkout preparation to the Shopping Agent.
- Delegate upsell analysis, cross-sell recommendations, and merchant revenue campaigns to the Growth Agent.
- Delegate financial breakdown, money safety authorization, and AP2/Razorpay payment execution to the Payment Agent.
"""

class RootAgent(Agent):
    name: str = "root_agent"
    description: str = "Root Orchestrator for AI Growth and Agentic Commerce."
    instruction: str = ROOT_INSTRUCTION

def create_root_agent() -> RootAgent:
    shopping = create_shopping_agent()
    growth = create_growth_agent()
    payment = create_payment_agent()

    return RootAgent(
        model=config.google_genai_model,
        instruction=ROOT_INSTRUCTION,
        # In Google ADK sub-agents are passed/attached to root agent
        sub_agents=[shopping, growth, payment] if hasattr(Agent, "sub_agents") else []
    )
