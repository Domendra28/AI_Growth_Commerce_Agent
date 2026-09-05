import os
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class AppConfig(BaseModel):
    google_api_key: str = Field(default_factory=lambda: os.getenv("GOOGLE_API_KEY", "mock_google_key"))
    google_genai_model: str = Field(default_factory=lambda: os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.5-flash"))
    
    razorpay_key_id: str = Field(default_factory=lambda: os.getenv("RAZORPAY_KEY_ID", "rzp_test_mock123"))
    razorpay_key_secret: str = Field(default_factory=lambda: os.getenv("RAZORPAY_KEY_SECRET", "mock_secret_456"))
    razorpay_mode: str = Field(default_factory=lambda: os.getenv("RAZORPAY_MODE", "test"))
    
    ucp_base_url: str = Field(default_factory=lambda: os.getenv("UCP_BASE_URL", "http://mock-ucp.local"))
    ap2_base_url: str = Field(default_factory=lambda: os.getenv("AP2_BASE_URL", "http://mock-ap2.local"))
    
    payment_provider: str = Field(default_factory=lambda: os.getenv("PAYMENT_PROVIDER", "mock"))
    
    max_transaction_amount: float = Field(default_factory=lambda: float(os.getenv("MAX_TRANSACTION_AMOUNT", "10000")))
    allowed_currency: str = Field(default_factory=lambda: os.getenv("ALLOWED_CURRENCY", "INR"))
    allowed_merchants: List[str] = Field(
        default_factory=lambda: os.getenv("ALLOWED_MERCHANTS", "TechStore,FashionHub,GeneralStore").split(",")
    )
    max_quantity: int = Field(default_factory=lambda: int(os.getenv("MAX_QUANTITY", "5")))
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

config = AppConfig()
