import pytest
import json
from app.agent import CommerceAgentSystem
from app.protocols.ucp.client import UCPClient
from app.tools.payment_tools import execute_ap2_payment_tool
from app.tools.checkout_tools import create_cart_tool

def test_out_of_stock_product_handling():
    ucp = UCPClient()
    with pytest.raises(ValueError, match="Insufficient stock"):
        ucp.create_cart(merchant_id="TechStore", items=[{"product_id": "prod_out_of_stock", "quantity": 1}])

def test_exceed_max_quantity_limit():
    res_str = create_cart_tool(merchant_id="TechStore", product_id="prod_laptop_basic", quantity=10)
    data = json.loads(res_str)
    assert data["status"] == "error"
    assert "exceeds maximum allowed limit" in data["message"]

def test_exceeds_max_transaction_amount():
    system = CommerceAgentSystem()
    cart_res = system.process_cart_creation("TechStore", "prod_laptop_basic", quantity=1)
    cart_id = cart_res["cart"]["cart_id"]
    checkout_res = system.process_checkout_preparation(cart_id)
    order_id = checkout_res["order"]["order_id"]

    pay_res = system.process_payment_execution(order_id=order_id, user_authorized=True)
    assert pay_res["status"] == "error"
    assert pay_res["error_code"] == "EXCEEDS_MAX_AMOUNT"

def test_missing_user_authorization_gate():
    system = CommerceAgentSystem()
    cart_res = system.process_cart_creation("TechStore", "prod_mouse_wireless", quantity=1)
    cart_id = cart_res["cart"]["cart_id"]
    checkout_res = system.process_checkout_preparation(cart_id)
    order_id = checkout_res["order"]["order_id"]

    pay_res = system.process_payment_execution(order_id=order_id, user_authorized=False)
    assert pay_res["status"] == "requires_user_authorization"

def test_payment_failure_and_recovery():
    system = CommerceAgentSystem()
    cart_res = system.process_cart_creation("TechStore", "prod_mouse_wireless", quantity=1)
    cart_id = cart_res["cart"]["cart_id"]
    checkout_res = system.process_checkout_preparation(cart_id)
    order_id = checkout_res["order"]["order_id"]

    # Execute with simulated failure
    pay_res = system.process_payment_execution(order_id=order_id, user_authorized=True, simulate_failure=True)
    assert pay_res["status"] == "failed"
    assert "safe_next_step" in pay_res
