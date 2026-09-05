from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from .cart import CartItem

class OrderStatus(str, Enum):
    CREATED = "CREATED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class Order(BaseModel):
    order_id: str
    cart_id: str
    merchant_id: str
    items: List[CartItem]
    total_amount: float
    currency: str = "INR"
    status: OrderStatus = OrderStatus.CREATED
    payment_id: Optional[str] = None
    razorpay_order_id: Optional[str] = None
    created_at: str
