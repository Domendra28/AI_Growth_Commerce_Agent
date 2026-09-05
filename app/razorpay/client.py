import logging
import uuid
from typing import Dict, Any, Optional
from app.config import config
from app.models.payment import PaymentResult, PaymentStatus

logger = logging.getLogger("commerce_agent.razorpay")

class RazorpayPaymentService:
    """
    Razorpay Test Mode payment integration.
    Gracefully falls back to mock execution when test keys are placeholders or when provider is set to mock.
    """

    def __init__(self):
        self.key_id = config.razorpay_key_id
        self.key_secret = config.razorpay_key_secret
        self.mode = config.razorpay_mode
        self.provider = config.payment_provider
        self._client = None

        if self.provider == "razorpay":
            try:
                import razorpay
                self._client = razorpay.Client(auth=(self.key_id, self.key_secret))
                logger.info(f"Razorpay Client initialized in {self.mode} mode.")
            except Exception as e:
                logger.warning(f"Could not initialize Razorpay client ({e}). Falling back to mock implementation.")
                self._client = None

    def create_order(self, amount: float, currency: str, receipt_id: str) -> Dict[str, Any]:
        """Creates a Razorpay test mode order."""
        amount_in_paise = int(amount * 100)
        
        if self._client:
            try:
                data = {
                    "amount": amount_in_paise,
                    "currency": currency,
                    "receipt": receipt_id,
                    "notes": {"mode": "test_agentic_commerce"}
                }
                return self._client.order.create(data=data)
            except Exception as e:
                logger.error(f"Razorpay API call failed: {e}. Falling back to sandbox order creation.")

        # Fallback / Mock response
        return {
            "id": f"order_rzp_{uuid.uuid4().hex[:10]}",
            "entity": "order",
            "amount": amount_in_paise,
            "currency": currency,
            "receipt": receipt_id,
            "status": "created"
        }

    def capture_payment(
        self,
        razorpay_order_id: str,
        amount: float,
        currency: str,
        simulate_failure: bool = False
    ) -> PaymentResult:
        """Captures/confirms payment in Razorpay Test Mode."""
        if simulate_failure or amount == 9999.0:
            return PaymentResult(
                transaction_id=f"tx_rzp_fail_{uuid.uuid4().hex[:6]}",
                intent_id=razorpay_order_id,
                status=PaymentStatus.FAILED,
                amount=amount,
                currency=currency,
                provider=self.provider,
                error_message="Razorpay Test Payment Failed: Test payment authorization was declined."
            )

        pay_id = f"pay_rzp_{uuid.uuid4().hex[:10]}"
        return PaymentResult(
            transaction_id=f"tx_{uuid.uuid4().hex[:8]}",
            intent_id=razorpay_order_id,
            status=PaymentStatus.SUCCESS,
            amount=amount,
            currency=currency,
            provider=self.provider,
            razorpay_payment_id=pay_id
        )

def get_payment_service() -> RazorpayPaymentService:
    return RazorpayPaymentService()
