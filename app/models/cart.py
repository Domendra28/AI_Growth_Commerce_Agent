from typing import List
from pydantic import BaseModel, Field
from .product import Product

class CartItem(BaseModel):
    product: Product
    quantity: int = 1

    @property
    def subtotal(self) -> float:
        return self.product.price * self.quantity

class Cart(BaseModel):
    cart_id: str
    merchant_id: str = "TechStore"
    items: List[CartItem] = Field(default_factory=list)
    currency: str = "INR"

    @property
    def total_amount(self) -> float:
        return sum(item.subtotal for item in self.items)
