import json
from typing import List, Dict, Any
from app.protocols.ucp.client import UCPClient
from app.audit.trail import get_audit_trail
from app.models.audit import AuditEventType
from app.config import config

ucp_client = UCPClient()
audit = get_audit_trail()

def create_cart_tool(
    merchant_id: str,
    product_id: str,
    quantity: int = 1,
    session_id: str = "default_session"
) -> str:
    """
    Create a shopping cart via UCP containing the requested product and quantity.
    Enforces maximum quantity bounds.
    """
    if quantity > config.max_quantity:
        return json.dumps({
            "status": "error",
            "message": f"Quantity {quantity} exceeds maximum allowed limit per item ({config.max_quantity})."
        })

    try:
        cart = ucp_client.create_cart(merchant_id, [{"product_id": product_id, "quantity": quantity}])
        audit.log_event(
            session_id=session_id,
            event_type=AuditEventType.CART_CREATED,
            agent="ShoppingAgent",
            tool="create_cart_tool",
            amount=cart.total_amount,
            currency=cart.currency,
            details={"cart_id": cart.cart_id, "items_count": len(cart.items)}
        )
        return json.dumps({"status": "success", "cart": cart.model_dump()}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def prepare_checkout_tool(
    cart_id: str,
    session_id: str = "default_session"
) -> str:
    """
    Convert an active cart into a formal merchant checkout order in UCP.
    Prepares complete transaction details (breakdown of price, quantity, totals).
    """
    try:
        order = ucp_client.create_order(cart_id)
        audit.log_event(
            session_id=session_id,
            event_type=AuditEventType.CHECKOUT_CREATED,
            agent="ShoppingAgent",
            tool="prepare_checkout_tool",
            order_id=order.order_id,
            amount=order.total_amount,
            currency=order.currency,
            details={"cart_id": cart_id, "status": order.status.value}
        )
        return json.dumps({"status": "success", "order": order.model_dump()}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
