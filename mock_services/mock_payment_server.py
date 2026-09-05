import uuid
from typing import Dict, Optional
from app.models.payment import PaymentIntent, PaymentResult, PaymentStatus

class MockPaymentServer:
    """Mock Agent Payments Protocol (AP2) server simulating payment processing."""

    def __init__(self):
        self.intents: Dict[str, PaymentIntent] = {}
        self.transactions: Dict[str, PaymentResult] = {}
        self.should_fail_next: bool = False

    def create_intent(self, amount: float, currency: str, merchant_id: str, order_id: str, reason: str) -> PaymentIntent:
        intent_id = f"pi_{uuid.uuid4().hex[:8]}"
        intent = PaymentIntent(
            intent_id=intent_id,
            amount=amount,
            currency=currency,
            merchant_id=merchant_id,
            order_id=order_id,
            reason=reason
        )
        self.intents[intent_id] = intent
        return intent

    def execute_payment(self, intent_id: str, user_authorized: bool, simulate_failure: bool = False) -> PaymentResult:
        if intent_id not in self.intents:
            raise ValueError(f"Payment intent {intent_id} not found.")

        intent = self.intents[intent_id]

        if not user_authorized:
            tx_id = f"tx_{uuid.uuid4().hex[:8]}"
            result = PaymentResult(
                transaction_id=tx_id,
                intent_id=intent_id,
                status=PaymentStatus.FAILED,
                amount=intent.amount,
                currency=intent.currency,
                provider="mock",
                error_message="Payment rejected: User authorization was not granted."
            )
            self.transactions[tx_id] = result
            return result

        if simulate_failure or self.should_fail_next or intent.amount == 9999.0:
            self.should_fail_next = False
            tx_id = f"tx_{uuid.uuid4().hex[:8]}"
            result = PaymentResult(
                transaction_id=tx_id,
                intent_id=intent_id,
                status=PaymentStatus.FAILED,
                amount=intent.amount,
                currency=intent.currency,
                provider="mock",
                error_message="Card authorization failed: Insufficient test funds or bank card declined."
            )
            self.transactions[tx_id] = result
            return result

        tx_id = f"tx_{uuid.uuid4().hex[:8]}"
        result = PaymentResult(
            transaction_id=tx_id,
            intent_id=intent_id,
            status=PaymentStatus.SUCCESS,
            amount=intent.amount,
            currency=intent.currency,
            provider="mock",
            razorpay_payment_id=f"pay_mock_{uuid.uuid4().hex[:8]}"
        )
        self.transactions[tx_id] = result
        return result

_mock_payment_server = MockPaymentServer()

def get_mock_payment_server() -> MockPaymentServer:
    return _mock_payment_server
