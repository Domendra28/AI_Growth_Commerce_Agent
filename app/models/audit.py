from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel

class AuditEventType(str, Enum):
    SESSION_STARTED = "SESSION_STARTED"
    USER_REQUEST_RECEIVED = "USER_REQUEST_RECEIVED"
    PRODUCT_SEARCHED = "PRODUCT_SEARCHED"
    PRODUCT_RECOMMENDED = "PRODUCT_RECOMMENDED"
    UPSELL_RECOMMENDED = "UPSELL_RECOMMENDED"
    CROSS_SELL_RECOMMENDED = "CROSS_SELL_RECOMMENDED"
    CART_CREATED = "CART_CREATED"
    CHECKOUT_CREATED = "CHECKOUT_CREATED"
    TRANSACTION_CALCULATED = "TRANSACTION_CALCULATED"
    AUTHORIZATION_REQUESTED = "AUTHORIZATION_REQUESTED"
    AUTHORIZATION_GRANTED = "AUTHORIZATION_GRANTED"
    PAYMENT_INITIATED = "PAYMENT_INITIATED"
    PAYMENT_SUCCEEDED = "PAYMENT_SUCCEEDED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    ORDER_CREATED = "ORDER_CREATED"
    ORDER_CONFIRMED = "ORDER_CONFIRMED"
    CAMPAIGN_RECOMMENDED = "CAMPAIGN_RECOMMENDED"

class AuditEvent(BaseModel):
    timestamp: str
    session_id: str
    event_type: AuditEventType
    agent: str
    tool: Optional[str] = None
    transaction_id: Optional[str] = None
    order_id: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    authorization_state: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
