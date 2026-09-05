from typing import List, Dict, Any, Optional
import json
from google.adk import Agent
from app.tools.catalog_tools import search_catalog_tool, get_product_details_tool
from app.tools.checkout_tools import create_cart_tool, prepare_checkout_tool
from app.config import config

SHOPPING_INSTRUCTION = """
You are the UCP Shopping Agent for Agentic Commerce.
Your role is to help AI buyers and shoppers discover products, compare features, inspect merchant catalogs, create carts, and prepare checkout orders.

Always follow these guidelines:
1. Search products accurately using UCP catalog tools based on the user's intent, category, or budget.
2. Provide objective product comparisons and highlight availability.
3. Help the user select the best matching product, add it to cart, and prepare checkout.
"""

class ShoppingAgent(Agent):
    name: str = "shopping_agent"
    description: str = "Handles merchant product discovery, UCP catalog lookups, product comparisons, cart creation, and checkout preparation."
    instruction: str = SHOPPING_INSTRUCTION
    tools: List[Any] = [search_catalog_tool, get_product_details_tool, create_cart_tool, prepare_checkout_tool]

def create_shopping_agent() -> ShoppingAgent:
    return ShoppingAgent(
        model=config.google_genai_model,
        instruction=SHOPPING_INSTRUCTION,
        tools=[search_catalog_tool, get_product_details_tool, create_cart_tool, prepare_checkout_tool]
    )
