import json
import uuid
import unittest

class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

class Inventory:
    def __init__(self, catalog_data):
        self.products = {}
        for item in catalog_data:
            self.products[item['id']] = Product(item['id'], item['name'], item['price'], item['stock'])

    def get_product(self, pid):
        if pid not in self.products:
            raise ValueError(f"Product {pid} not found.")
        return self.products[pid]

class Cart:
    def __init__(self):
        self.items = {} 

    def add_item(self, product_id, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        self.items[product_id] = self.items.get(product_id, 0) + quantity

class Order:
    def __init__(self, inventory: Inventory, cart: Cart, discount_pct=0.0):
        self.order_id = str(uuid.uuid4())
        self.inventory = inventory
        self.discount_pct = discount_pct
        self.items_snapshot = []
        self.total_amount = 0.0
        self._validate_and_prepare(cart)

    def _validate_and_prepare(self, cart):
    
        for pid, qty in cart.items.items():
            product = self.inventory.get_product(pid)
            if product.stock < qty:
                raise ValueError(f"Out of stock for product {pid}. Available: {product.stock}, requested: {qty}")
            self.items_snapshot.append({'product_id': pid, 'price': product.price, 'quantity': qty})

        subtotal = sum(item['price'] * item['quantity'] for item in self.items_snapshot)
        self.total_amount = subtotal * (1.0 - self.discount_pct / 100.0)

    def fulfill(self):
        # Deduct stock
        for item in self.items_snapshot:
            product = self.inventory.get_product(item['product_id'])
            product.stock -= item['quantity']

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "items": self.items_snapshot,
            "total": self.total_amount
        }

class TestOrderSystem(unittest.TestCase):
    def test_successful_order(self):
        cat = [{"id": "P1", "name": "Widget", "price": 100, "stock": 5}]
        inv = Inventory(cat)
        cart = Cart()
        cart.add_item("P1", 2)
        order = Order(inv, cart, discount_pct=10.0)
        self.assertEqual(order.total_amount, 180.0)
        order.fulfill()
        self.assertEqual(inv.get_product("P1").stock, 3)

    def test_out_of_stock(self):
        cat = [{"id": "P1", "name": "Widget", "price": 100, "stock": 1}]
        inv = Inventory(cat)
        cart = Cart()
        cart.add_item("P1", 2)
        with self.assertRaises(ValueError):
            Order(inv, cart)

    def test_invalid_quantity(self):
        cart = Cart()
        with self.assertRaises(ValueError):
            cart.add_item("P1", 0)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)