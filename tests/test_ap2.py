import pytest
from app.protocols.ap2.client import AP2Client
from app.models.payment import PaymentStatus

def test_ap2_intent_and_authorization():
    ap2 = AP2Client()

    intent = ap2.create_payment_intent(
        amount=1500.0,
        currency="INR",
        merchant_id="TechStore",
        order_id="ord_test1",
        reason="Purchase accessories"
    )

    assert intent.intent_id.startswith("pi_")
    assert intent.amount == 1500.0

    # Authorization Request
    auth_req = ap2.prepare_authorization_request(intent, explanation="Test purchase breakdown")
    assert auth_req.user_authorized is False

    # Execute without auth
    unauth_res = ap2.execute_payment(intent.intent_id, user_authorized=False)
    assert unauth_res.status == PaymentStatus.FAILED

    # Execute with auth
    auth_res = ap2.execute_payment(intent.intent_id, user_authorized=True)
    assert auth_res.status == PaymentStatus.SUCCESS
