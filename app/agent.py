import json
import logging
from typing import Dict, Any, Optional
from app.agents.root_agent import create_root_agent
from app.agents.shopping_agent import create_shopping_agent
from app.agents.growth_agent import create_growth_agent
from app.agents.payment_agent import create_payment_agent
from app.tools.catalog_tools import search_catalog_tool, get_product_details_tool
from app.tools.checkout_tools import create_cart_tool, prepare_checkout_tool
from app.tools.growth_tools import analyze_upsell_tool, analyze_cross_sell_tool, orchestrate_campaign_tool
from app.tools.payment_tools import execute_ap2_payment_tool
from app.audit.trail import get_audit_trail
from app.models.audit import AuditEventType

logger = logging.getLogger("commerce_agent.main")

class CommerceAgentSystem:
    """
    Main system wrapper encapsulating the Root Agent, sub-agents, UCP, AP2, and safety audit trail.
    Provides direct API methods for programmatic invocation, testing, and CLI interaction.
    """

    def __init__(self):
        self.root_agent = create_root_agent()
        self.shopping_agent = create_shopping_agent()
        self.growth_agent = create_growth_agent()
        self.payment_agent = create_payment_agent()
        self.audit = get_audit_trail()

    def process_shopping_intent(
        self,
        query: str,
        max_price: Optional[float] = None,
        category: Optional[str] = None,
        session_id: str = "demo_session"
    ) -> Dict[str, Any]:
        """Handles natural language product search & discovery."""
        self.audit.log_event(
            session_id=session_id,
            event_type=AuditEventType.USER_REQUEST_RECEIVED,
            agent="RootAgent",
            details={"query": query, "max_price": max_price, "category": category}
        )
        res_str = search_catalog_tool(query=query, max_price=max_price, category=category, session_id=session_id)
        return json.loads(res_str)

    def process_upsell_analysis(self, product_id: str, session_id: str = "demo_session") -> Dict[str, Any]:
        """Queries AI Growth agent for upsell recommendations."""
        res_str = analyze_upsell_tool(product_id=product_id, session_id=session_id)
        return json.loads(res_str)

    def process_cross_sell_analysis(self, product_id: str, session_id: str = "demo_session") -> Dict[str, Any]:
        """Queries AI Growth agent for cross-sell accessories."""
        res_str = analyze_cross_sell_tool(product_id=product_id, session_id=session_id)
        return json.loads(res_str)

    def process_cart_creation(
        self,
        merchant_id: str,
        product_id: str,
        quantity: int = 1,
        session_id: str = "demo_session"
    ) -> Dict[str, Any]:
        """Adds product to cart via UCP."""
        res_str = create_cart_tool(merchant_id=merchant_id, product_id=product_id, quantity=quantity, session_id=session_id)
        return json.loads(res_str)

    def process_checkout_preparation(self, cart_id: str, session_id: str = "demo_session") -> Dict[str, Any]:
        """Prepares checkout order via UCP."""
        res_str = prepare_checkout_tool(cart_id=cart_id, session_id=session_id)
        return json.loads(res_str)

    def process_payment_execution(
        self,
        order_id: str,
        user_authorized: bool = False,
        simulate_failure: bool = False,
        session_id: str = "demo_session"
    ) -> Dict[str, Any]:
        """Executes payment via AP2 subject to user authorization and transaction bounds."""
        res_str = execute_ap2_payment_tool(
            order_id=order_id,
            user_authorized=user_authorized,
            simulate_failure=simulate_failure,
            session_id=session_id
        )
        return json.loads(res_str)

    def process_campaign_orchestration(
        self,
        merchant_id: str,
        goal: str = "increase_average_order_value",
        merchant_authorized: bool = False,
        session_id: str = "demo_session"
    ) -> Dict[str, Any]:
        """Orchestrates AI Growth campaign for merchant."""
        res_str = orchestrate_campaign_tool(
            merchant_id=merchant_id,
            goal=goal,
            merchant_authorized=merchant_authorized,
            session_id=session_id
        )
        return json.loads(res_str)
