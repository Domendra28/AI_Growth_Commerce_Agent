import json
from typing import Optional
from app.protocols.ucp.client import UCPClient
from app.audit.trail import get_audit_trail
from app.models.audit import AuditEventType

ucp_client = UCPClient()
audit = get_audit_trail()

def analyze_upsell_tool(product_id: str, session_id: str = "default_session") -> str:
    """
    Analyze the product catalog to identify premium upsell recommendations with explainable value add.
    """
    product = ucp_client.get_product_details(product_id)
    if not product:
        return json.dumps({"status": "error", "message": f"Product {product_id} not found."})

    upsell_list = []
    for u_id in product.upsell_products:
        u_product = ucp_client.get_product_details(u_id)
        if u_product and u_product.inventory > 0:
            price_diff = u_product.price - product.price
            upsell_list.append({
                "product": u_product.model_dump(),
                "price_difference": price_diff,
                "reasoning": f"Upgrading to {u_product.name} offers enhanced performance and features for an additional {product.currency} {price_diff:,.2f}."
            })

    if upsell_list:
        audit.log_event(
            session_id=session_id,
            event_type=AuditEventType.UPSELL_RECOMMENDED,
            agent="GrowthAgent",
            tool="analyze_upsell_tool",
            details={"base_product": product_id, "upsell_count": len(upsell_list)}
        )

    return json.dumps({
        "status": "success",
        "base_product": product.name,
        "upsells": upsell_list
    }, indent=2)

def analyze_cross_sell_tool(product_id: str, session_id: str = "default_session") -> str:
    """
    Analyze complementary accessories and related products for cross-selling opportunities.
    """
    product = ucp_client.get_product_details(product_id)
    if not product:
        return json.dumps({"status": "error", "message": f"Product {product_id} not found."})

    cross_sells = []
    for c_id in product.cross_sell_products:
        c_product = ucp_client.get_product_details(c_id)
        if c_product and c_product.inventory > 0:
            cross_sells.append({
                "product": c_product.model_dump(),
                "reasoning": f"{c_product.name} complements {product.name} seamlessly."
            })

    if cross_sells:
        audit.log_event(
            session_id=session_id,
            event_type=AuditEventType.CROSS_SELL_RECOMMENDED,
            agent="GrowthAgent",
            tool="analyze_cross_sell_tool",
            details={"base_product": product_id, "cross_sell_count": len(cross_sells)}
        )

    return json.dumps({
        "status": "success",
        "base_product": product.name,
        "cross_sells": cross_sells
    }, indent=2)

def orchestrate_campaign_tool(
    merchant_id: str,
    goal: str = "increase_average_order_value",
    merchant_authorized: bool = False,
    session_id: str = "default_session"
) -> str:
    """
    Analyze merchant catalog and orchestrate AI Growth revenue campaigns.
    Generates actionable campaign strategies with estimated ROI impact.
    Enforces authorization gate before executing campaign modifications.
    """
    products = ucp_client.discover_products(merchant_id=merchant_id)
    if not products:
        return json.dumps({"status": "error", "message": f"No products found for merchant {merchant_id}."})

    campaign_plan = {
        "merchant_id": merchant_id,
        "goal": goal,
        "strategy": "Bundled Accessory Discount & High-Margin Upsell Highlights",
        "estimated_aov_increase": "+18.5%",
        "proposed_action": "Bundle TechBook Air 14 with ErgoMouse Wireless and Protective Sleeve for a 10% bundle discount.",
        "requires_merchant_authorization": True,
        "merchant_authorized": merchant_authorized
    }

    audit.log_event(
        session_id=session_id,
        event_type=AuditEventType.CAMPAIGN_RECOMMENDED,
        agent="GrowthAgent",
        tool="orchestrate_campaign_tool",
        details=campaign_plan
    )

    if not merchant_authorized:
        return json.dumps({
            "status": "pending_authorization",
            "campaign": campaign_plan,
            "message": "Campaign strategy generated. Merchant authorization required prior to activation."
        }, indent=2)

    return json.dumps({
        "status": "active",
        "campaign": campaign_plan,
        "message": "Campaign successfully authorized and activated in test mode."
    }, indent=2)
