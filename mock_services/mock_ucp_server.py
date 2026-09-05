import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderStatus
from app.models.product import Product


class MockUCPServer:
	"""In-memory UCP server used by the local demo and test suite."""

	def __init__(self):
		self.products: Dict[str, Product] = {
			"prod_laptop_basic": Product(
				product_id="prod_laptop_basic",
				name="Essential Laptop",
				description="Reliable laptop for everyday work and study.",
				category="electronics",
				price=15000.0,
				merchant_id="TechStore",
				inventory=10,
				cross_sell_products=["prod_mouse_wireless"],
			),
			"prod_mouse_wireless": Product(
				product_id="prod_mouse_wireless",
				name="Wireless Mouse",
				description="Comfortable wireless mouse with silent clicks.",
				category="electronics",
				price=799.0,
				merchant_id="TechStore",
				inventory=25,
			),
			"prod_runner_shoes": Product(
				product_id="prod_runner_shoes",
				name="Runner Pro Shoes",
				description="Lightweight running shoes for daily training.",
				category="footwear",
				price=3499.0,
				merchant_id="FashionHub",
				inventory=12,
				cross_sell_products=["prod_sports_socks"],
			),
			"prod_sports_socks": Product(
				product_id="prod_sports_socks",
				name="Sports Socks",
				description="Breathable socks designed for running and training.",
				category="accessories",
				price=499.0,
				merchant_id="FashionHub",
				inventory=30,
			),
			"prod_out_of_stock": Product(
				product_id="prod_out_of_stock",
				name="Out of Stock Product",
				description="Product reserved for inventory failure tests.",
				category="general",
				price=100.0,
				merchant_id="TechStore",
				inventory=0,
			),
		}
		self.carts: Dict[str, Cart] = {}
		self.orders: Dict[str, Order] = {}

	def discover_products(
		self,
		query: Optional[str] = None,
		category: Optional[str] = None,
		max_price: Optional[float] = None,
		merchant_id: Optional[str] = None,
	) -> List[Product]:
		query_text = query.lower().strip() if query else None
		return [
			product
			for product in self.products.values()
			if (not query_text or query_text in product.name.lower() or query_text in product.description.lower())
			and (not category or product.category.lower() == category.lower())
			and (max_price is None or product.price <= max_price)
			and (not merchant_id or product.merchant_id == merchant_id)
			and product.inventory > 0
		]

	def get_product(self, product_id: str) -> Optional[Product]:
		return self.products.get(product_id)

	def create_cart(self, merchant_id: str, items: List[Dict[str, Any]]) -> Cart:
		cart_items: List[CartItem] = []
		for item in items:
			product = self.get_product(item["product_id"])
			if product is None:
				raise ValueError(f"Product {item['product_id']} not found.")

			quantity = item.get("quantity", 1)
			if product.inventory < quantity:
				raise ValueError(f"Insufficient stock for product {product.product_id}.")
			cart_items.append(CartItem(product=product, quantity=quantity))

		cart = Cart(
			cart_id=f"cart_{uuid.uuid4().hex[:8]}",
			merchant_id=merchant_id,
			items=cart_items,
		)
		self.carts[cart.cart_id] = cart
		return cart

	def get_cart(self, cart_id: str) -> Optional[Cart]:
		return self.carts.get(cart_id)

	def create_order(self, cart_id: str) -> Order:
		cart = self.get_cart(cart_id)
		if cart is None:
			raise ValueError(f"Cart {cart_id} not found.")

		order = Order(
			order_id=f"order_{uuid.uuid4().hex[:8]}",
			cart_id=cart.cart_id,
			merchant_id=cart.merchant_id,
			items=cart.items,
			total_amount=cart.total_amount,
			currency=cart.currency,
			created_at=datetime.now(timezone.utc).isoformat(),
		)
		self.orders[order.order_id] = order
		return order

	def get_order(self, order_id: str) -> Optional[Order]:
		return self.orders.get(order_id)

	def update_order_status(
		self,
		order_id: str,
		status: OrderStatus,
		payment_id: Optional[str] = None,
	) -> Order:
		order = self.get_order(order_id)
		if order is None:
			raise ValueError(f"Order {order_id} not found.")

		order.status = status
		if payment_id is not None:
			order.payment_id = payment_id
		self.orders[order_id] = order
		return order


_mock_ucp_server = MockUCPServer()


def get_mock_ucp_server() -> MockUCPServer:
	return _mock_ucp_server
