import pytest
from app.razorpay.client import RazorpayPaymentService
from app.models.payment import PaymentStatus

def test_razorpay_order_creation_and_capture():
    service = RazorpayPaymentService()

    order_info = service.create_order(amount=2000.0, currency="INR", receipt_id="rec_001")
    assert "id" in order_info

    pay_res = service.capture_payment(razorpay_order_id=order_info["id"], amount=2000.0, currency="INR")
    assert pay_res.status == PaymentStatus.SUCCESS
    assert pay_res.amount == 2000.0
