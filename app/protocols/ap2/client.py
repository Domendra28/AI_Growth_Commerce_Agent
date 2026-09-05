from typing import Optional
from app.models.payment import PaymentIntent, AuthorizationRequest, PaymentResult, PaymentStatus
from app.config import config
from mock_services.mock_payment_server import get_mock_payment_server

class AP2Client:
    """
    Agent Payments Protocol (AP2) Client Adapter.
    Encapsulates financial transaction boundaries: Payment Intent creation,
    explicit user authorization checks, payment request dispatching, and confirmation.
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url
        self._mock_server = get_mock_payment_server()

    def create_payment_intent(
        self,
        amount: float,
        currency: str,
        merchant_id: str,
        order_id: str,
        reason: str
    ) -> PaymentIntent:
        """Create AP2 Payment Intent."""
        return self._mock_server.create_intent(
            amount=amount,
            currency=currency,
            merchant_id=merchant_id,
            order_id=order_id,
            reason=reason
        )

    def prepare_authorization_request(
        self,
        intent: PaymentIntent,
        explanation: str
    ) -> AuthorizationRequest:
        """Prepare an explainable authorization prompt for user gating."""
        return AuthorizationRequest(
            intent_id=intent.intent_id,
            amount=intent.amount,
            currency=intent.currency,
            merchant_id=intent.merchant_id,
            explanation=explanation,
            user_authorized=False
        )

    def execute_payment(
        self,
        intent_id: str,
        user_authorized: bool,
        simulate_failure: bool = False
    ) -> PaymentResult:
        """Execute AP2 payment transaction subject to money safety gates."""
        if not user_authorized:
            return PaymentResult(
                transaction_id="tx_unauthorized",
                intent_id=intent_id,
                status=PaymentStatus.FAILED,
                amount=0.0,
                currency=config.allowed_currency,
                provider=config.payment_provider,
                error_message="AUTHORIZATION REJECTED: User did not explicitly approve payment."
            )

        return self._mock_server.execute_payment(
            intent_id=intent_id,
            user_authorized=user_authorized,
            simulate_failure=simulate_failure
        )
