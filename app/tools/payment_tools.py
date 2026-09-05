import json
from app.protocols.ap2.client import AP2Client
from app.protocols.ucp.client import UCPClient
from app.razorpay.client import get_payment_service
from app.audit.trail import get_audit_trail
from app.models.audit import AuditEventType
from app.models.order import OrderStatus
from app.models.payment import PaymentStatus
from app.config import config

ap2_client = AP2Client()
ucp_client = UCPClient()
payment_service = get_payment_service()
audit = get_audit_trail()

def execute_ap2_payment_tool(
    order_id: str,
    user_authorized: bool = False,
    simulate_failure: bool = False,
    session_id: str = "default_session"
) -> str:
    """
    Execute AP2 Payment flow using Razorpay Test Mode or Mock Payment Provider.
    Enforces Money Safety: Explainability, Transaction Bounding, and Explicit User Authorization Gating.
    """
    order = ucp_client.get_order_status(order_id)
    if not order:
        return json.dumps({"status": "error", "message": f"Order {order_id} not found."})

    # 1. Bounded Safety Verification
    if order.total_amount > config.max_transaction_amount:
        error_msg = f"TRANSACTION REFUSED: Order total ({order.currency} {order.total_amount:,.2f}) exceeds max allowed transaction limit ({config.allowed_currency} {config.max_transaction_amount:,.2f})."
        audit.log_event(
            session_id=session_id,
            event_type=AuditEventType.PAYMENT_FAILED,
            agent="PaymentAgent",
            tool="execute_ap2_payment_tool",
            order_id=order_id,
            amount=order.total_amount,
            currency=order.currency,
            error=error_msg
        )
        return json.dumps({"status": "error", "error_code": "EXCEEDS_MAX_AMOUNT", "message": error_msg})

    if order.merchant_id not in config.allowed_merchants:
        error_msg = f"TRANSACTION REFUSED: Merchant '{order.merchant_id}' is not in allowed merchants list."
        audit.log_event(
            session_id=session_id,
            event_type=AuditEventType.PAYMENT_FAILED,
            agent="PaymentAgent",
            tool="execute_ap2_payment_tool",
            order_id=order_id,
            error=error_msg
        )
        return json.dumps({"status": "error", "error_code": "DISALLOWED_MERCHANT", "message": error_msg})

    # 2. Explainable Breakdown Preparation
    items_summary = [
        f"{i.quantity}x {i.product.name} @ {order.currency} {i.product.price:,.2f}"
        for i in order.items
    ]
    explanation = (
        f"TRANSACTION EXPLANATION:\n"
        f"Merchant: {order.merchant_id}\n"
        f"Order ID: {order.order_id}\n"
        f"Items: {', '.join(items_summary)}\n"
        f"Final Amount: {order.currency} {order.total_amount:,.2f}\n"
        f"Payment Mechanism: AP2 Gateway via {config.payment_provider.upper()} Test Mode"
    )

    # Log Intent & Calculation
    intent = ap2_client.create_payment_intent(
        amount=order.total_amount,
        currency=order.currency,
        merchant_id=order.merchant_id,
        order_id=order_id,
        reason=f"Purchase of {len(order.items)} item(s) from {order.merchant_id}"
    )

    audit.log_event(
        session_id=session_id,
        event_type=AuditEventType.TRANSACTION_CALCULATED,
        agent="PaymentAgent",
        tool="execute_ap2_payment_tool",
        transaction_id=intent.intent_id,
        order_id=order_id,
        amount=order.total_amount,
        currency=order.currency,
        details={"explanation": explanation}
    )

    # 3. Explicit Authorization Gating
    audit.log_event(
        session_id=session_id,
        event_type=AuditEventType.AUTHORIZATION_REQUESTED,
        agent="PaymentAgent",
        tool="execute_ap2_payment_tool",
        transaction_id=intent.intent_id,
        order_id=order_id,
        authorization_state="PENDING",
        details={"explanation": explanation}
    )

    if not user_authorized:
        return json.dumps({
            "status": "requires_user_authorization",
            "transaction_explanation": explanation,
            "payment_intent": intent.model_dump(),
            "message": "User explicit authorization is REQUIRED before executing financial transaction."
        }, indent=2)

    audit.log_event(
        session_id=session_id,
        event_type=AuditEventType.AUTHORIZATION_GRANTED,
        agent="PaymentAgent",
        tool="execute_ap2_payment_tool",
        transaction_id=intent.intent_id,
        order_id=order_id,
        authorization_state="GRANTED"
    )

    # 4. Initiate & Execute Payment (AP2 -> Razorpay/Mock)
    audit.log_event(
        session_id=session_id,
        event_type=AuditEventType.PAYMENT_INITIATED,
        agent="PaymentAgent",
        tool="execute_ap2_payment_tool",
        transaction_id=intent.intent_id,
        order_id=order_id,
        amount=order.total_amount,
        currency=order.currency
    )

    if config.payment_provider == "razorpay":
        rzp_order = payment_service.create_order(
            amount=order.total_amount,
            currency=order.currency,
            receipt_id=order_id
        )
        payment_result = payment_service.capture_payment(
            razorpay_order_id=rzp_order["id"],
            amount=order.total_amount,
            currency=order.currency,
            simulate_failure=simulate_failure
        )
    else:
        payment_result = ap2_client.execute_payment(
            intent_id=intent.intent_id,
            user_authorized=user_authorized,
            simulate_failure=simulate_failure
        )

    # 5. Handle Payment Result & Confirm Order
    if payment_result.status == PaymentStatus.SUCCESS:
        updated_order = ucp_client.update_order_status(
            order_id=order_id,
            status=OrderStatus.CONFIRMED,
            payment_id=payment_result.transaction_id
        )

        audit.log_event(
            session_id=session_id,
            event_type=AuditEventType.PAYMENT_SUCCEEDED,
            agent="PaymentAgent",
            tool="execute_ap2_payment_tool",
            transaction_id=payment_result.transaction_id,
            order_id=order_id,
            amount=payment_result.amount,
            currency=payment_result.currency,
            result="SUCCESS"
        )
        audit.log_event(
            session_id=session_id,
            event_type=AuditEventType.ORDER_CONFIRMED,
            agent="PaymentAgent",
            tool="execute_ap2_payment_tool",
            order_id=order_id,
            result="CONFIRMED"
        )

        return json.dumps({
            "status": "success",
            "message": "Payment executed and order confirmed successfully!",
            "transaction": payment_result.model_dump(),
            "order": updated_order.model_dump()
        }, indent=2)

    else:
        ucp_client.update_order_status(order_id=order_id, status=OrderStatus.FAILED)
        
        audit.log_event(
            session_id=session_id,
            event_type=AuditEventType.PAYMENT_FAILED,
            agent="PaymentAgent",
            tool="execute_ap2_payment_tool",
            transaction_id=payment_result.transaction_id,
            order_id=order_id,
            amount=payment_result.amount,
            error=payment_result.error_message or "Payment execution failed."
        )

        return json.dumps({
            "status": "failed",
            "message": f"Payment failed: {payment_result.error_message}",
            "transaction": payment_result.model_dump(),
            "safe_next_step": "Please verify payment credentials, check balance, or try another payment method."
        }, indent=2)
