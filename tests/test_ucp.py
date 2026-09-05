import pytest
from app.protocols.ucp.client import UCPClient
from app.models.order import OrderStatus

def test_ucp_full_lifecycle():
    client = UCPClient()

    # 1. Product discovery
    products = client.discover_products(merchant_id="FashionHub")
    assert len(products) > 0
    p = products[0]

    # 2. Cart creation
    cart = client.create_cart(merchant_id="FashionHub", items=[{"product_id": p.product_id, "quantity": 1}])
    assert cart.cart_id is not None
    assert cart.total_amount == p.price

    # 3. Checkout preparation & Order creation
    order = client.create_order(cart.cart_id)
    assert order.order_id is not None
    assert order.status == OrderStatus.CREATED

    # 4. Status update
    updated_order = client.update_order_status(order.order_id, OrderStatus.CONFIRMED, payment_id="tx_123")
    assert updated_order.status == OrderStatus.CONFIRMED
    assert updated_order.payment_id == "tx_123"
