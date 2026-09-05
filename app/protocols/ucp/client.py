from typing import List, Optional, Dict, Any
from app.models.product import Product
from app.models.cart import Cart
from app.models.order import Order, OrderStatus
from mock_services.mock_ucp_server import get_mock_ucp_server

class UCPClient:
    """
    Universal Commerce Protocol (UCP) Client Adapter.
    Acts as the standard interface for agent-driven merchant discovery, catalog inspection,
    cart management, checkout preparation, and order lifecycle management.
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url
        self._mock_server = get_mock_ucp_server()

    def discover_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        max_price: Optional[float] = None,
        merchant_id: Optional[str] = None
    ) -> List[Product]:
        """Search products using standard UCP discovery filtering."""
        return self._mock_server.discover_products(
            query=query, category=category, max_price=max_price, merchant_id=merchant_id
        )

    def get_product_details(self, product_id: str) -> Optional[Product]:
        """Retrieve complete product information and availability."""
        return self._mock_server.get_product(product_id)

    def create_cart(self, merchant_id: str, items: List[Dict[str, Any]]) -> Cart:
        """Create a standard UCP cart."""
        return self._mock_server.create_cart(merchant_id, items)

    def get_cart(self, cart_id: str) -> Optional[Cart]:
        """Retrieve cart state by cart_id."""
        return self._mock_server.get_cart(cart_id)

    def create_order(self, cart_id: str) -> Order:
        """Initiate order creation from an existing checkout cart."""
        return self._mock_server.create_order(cart_id)

    def update_order_status(self, order_id: str, status: OrderStatus, payment_id: Optional[str] = None) -> Order:
        """Update order lifecycle status in UCP backend."""
        return self._mock_server.update_order_status(order_id, status, payment_id)

    def get_order_status(self, order_id: str) -> Optional[Order]:
        """Retrieve current order details and status."""
        return self._mock_server.get_order(order_id)
