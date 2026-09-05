import json
from typing import Optional, Dict, Any
from app.protocols.ucp.client import UCPClient
from app.audit.trail import get_audit_trail
from app.models.audit import AuditEventType

ucp_client = UCPClient()
audit = get_audit_trail()

def search_catalog_tool(
    query: Optional[str] = None,
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    merchant_id: Optional[str] = None,
    session_id: str = "default_session"
) -> str:
    """
    Search the merchant product catalog via UCP protocol.
    Filters products by query, category, maximum price budget, and merchant.
    """
    products = ucp_client.discover_products(
        query=query, category=category, max_price=max_price, merchant_id=merchant_id
    )
    
    audit.log_event(
        session_id=session_id,
        event_type=AuditEventType.PRODUCT_SEARCHED,
        agent="ShoppingAgent",
        tool="search_catalog_tool",
        details={"query": query, "category": category, "max_price": max_price, "count": len(products)}
    )

    if not products:
        return json.dumps({"status": "empty", "message": "No matching products found.", "products": []})

    serialized = [p.model_dump() for p in products]
    return json.dumps({"status": "success", "count": len(products), "products": serialized}, indent=2)

def get_product_details_tool(product_id: str, session_id: str = "default_session") -> str:
    """
    Retrieve comprehensive details, specifications, inventory, and cross-sell/upsell relations for a product.
    """
    product = ucp_client.get_product_details(product_id)
    if not product:
        return json.dumps({"status": "error", "message": f"Product {product_id} not found."})

    return json.dumps({"status": "success", "product": product.model_dump()}, indent=2)
