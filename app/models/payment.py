from enum import Enum
from typing import Optional
from pydantic import BaseModel

class PaymentStatus(str, Enum):
    INITIATED = "INITIATED"
    AUTHORIZED = "AUTHORIZED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class PaymentIntent(BaseModel):
    intent_id: str
    amount: float
    currency: str
    merchant_id: str
    order_id: str
    reason: str

class AuthorizationRequest(BaseModel):
    intent_id: str
    amount: float
    currency: str
    merchant_id: str
    explanation: str
    user_authorized: bool = False

class PaymentResult(BaseModel):
    transaction_id: str
    intent_id: str
    status: PaymentStatus
    amount: float
    currency: str
    provider: str  # "razorpay" or "mock"
    razorpay_payment_id: Optional[str] = None
    error_message: Optional[str] = None
