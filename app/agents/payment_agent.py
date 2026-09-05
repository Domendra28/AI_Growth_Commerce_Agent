from typing import List, Any
from google.adk import Agent
from app.tools.payment_tools import execute_ap2_payment_tool
from app.config import config

PAYMENT_INSTRUCTION = """
You are the AP2 Payment Agent for Agentic Commerce.
Your primary duty is MONEY SAFETY and financial execution.

Rules:
1. Explainability: Always present a clear transaction breakdown (product, merchant, quantity, prices, taxes/fees, total amount, payment mechanism) before requesting approval.
2. Authorization Gate: Never execute a payment without explicit user approval (`user_authorized=True`).
3. Transaction Bounds: Automatically reject any transaction exceeding limits or disallowed merchants.
4. Failure Handling: If a payment fails, clearly explain why and provide safe next steps without blindly retrying.
"""

class PaymentAgent(Agent):
    name: str = "payment_agent"
    description: str = "Manages AP2 payment authorizations, money safety boundaries, Razorpay Test Mode execution, and failure handling."
    instruction: str = PAYMENT_INSTRUCTION
    tools: List[Any] = [execute_ap2_payment_tool]

def create_payment_agent() -> PaymentAgent:
    return PaymentAgent(
        model=config.google_genai_model,
        instruction=PAYMENT_INSTRUCTION,
        tools=[execute_ap2_payment_tool]
    )
