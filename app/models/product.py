from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class ProductAttribute(BaseModel):
    name: str
    value: str

class Product(BaseModel):
    product_id: str
    name: str
    description: str
    category: str
    price: float
    currency: str = "INR"
    merchant_id: str = "TechStore"
    inventory: int = 10
    image_url: str = ""
    badge: Optional[str] = None  # e.g. "Best Seller", "New", "Recommended"
    rating: float = 4.0
    review_count: int = 0
    attributes: Dict[str, Any] = Field(default_factory=dict)
    variants: List[Dict[str, Any]] = Field(default_factory=list)
    related_products: List[str] = Field(default_factory=list)
    upsell_products: List[str] = Field(default_factory=list)
    cross_sell_products: List[str] = Field(default_factory=list)
