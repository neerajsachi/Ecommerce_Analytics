from django.test import TestCase
from ecommerce.models import Category, Tag, Product, Customer, Order, OrderItem, Inventory
from django.utils import timezone
from decimal import Decimal


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Laptop", price=Decimal('1500.00'), SKU="LAPTOP123")
        self.inventory = Inventory.objects.create(product=self.product, quantity=10, last_restocked_date=timezone.now())


    def test_category_creation(self):
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(str(self.category), "Electronics")

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="New Arrival")

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "New Arrival")
        self.assertEqual(str(self.tag), "New Arrival")

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Laptop",
            description="High-end gaming laptop",
            SKU="ABC123",
            price=Decimal('1500.00'),
            category=self.category
        )
        

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Laptop")
        self.assertEqual(self.product.price, Decimal('1500.00'))
        self.assertEqual(str(self.product), "Laptop")

    def test_frequently_used_products(self):
        Inventory.objects.create(product=self.product, quantity=10, last_restocked_date=timezone.now())
        available_products = Product.frequently_used_products.available_products()
        self.assertIn(self.product, available_products)

class CustomerModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Phone", price=Decimal('500.00'), SKU="PHONE123")  # Create a Product instance
        self.customer = Customer.objects.create(
            name="John Doe",
            email="john@example.com",
            country="US"
        )
        self.inventory = Inventory.objects.create(product=self.product, quantity=10, last_restocked_date=timezone.now())  # Now this will work

    def test_customer_creation(self):
        self.assertEqual(self.customer.name, "John Doe")
        self.assertEqual(self.customer.email, "john@example.com")
        self.assertEqual(str(self.customer), "John Doe")

    def test_lifetime_value(self):
        order = Order.objects.create(customer=self.customer, total_amount=Decimal('1000.00'))
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=2, price_at_time_of_order=Decimal('500.00'))  # Use self.product
        lifetime_value = self.customer.lifetime_value()
        self.assertEqual(lifetime_value, Decimal('1000.00'))

class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="John Doe",
            email="john@example.com",
            country="US"
        )
        self.order = Order.objects.create(customer=self.customer, total_amount=Decimal('1000.00'))

    def test_order_creation(self):
        self.assertEqual(self.order.customer.name, "John Doe")
        self.assertEqual(self.order.total_amount, Decimal('1000.00'))
        self.assertEqual(self.order.status, 'PENDING')
        self.assertEqual(str(self.order), f"Order {self.order.id} for John Doe")

    def calculate_tax(self):
        country_tax_rates = {'US': Decimal('0.07'), 'UK': Decimal('0.20'), 'IN': Decimal('0.18')}
        default_tax_rate = Decimal('0.05') 
        tax_rate = country_tax_rates.get(self.customer.country, default_tax_rate)
        return self.total_amount * tax_rate
 
class OrderItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Laptop", price=Decimal('1500.00'), SKU="ABC123", category=self.category)
        self.inventory = Inventory.objects.create(product=self.product, quantity=10, last_restocked_date=timezone.now())
        self.customer = Customer.objects.create(name="John Doe", email="john@example.com", country="US")
        self.order = Order.objects.create(customer=self.customer, total_amount=Decimal('1500.00'))
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1, price_at_time_of_order=Decimal('1500.00'))

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.quantity, 1)
        self.assertEqual(self.order_item.price_at_time_of_order, Decimal('1500.00'))
        self.assertEqual(str(self.order_item), "1 of Laptop")

class InventoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Laptop", price=Decimal('1500.00'), SKU="ABC123", category=self.category)
        self.inventory = Inventory.objects.create(product=self.product, quantity=4, last_restocked_date=timezone.now())

    def test_inventory_creation(self):
        self.assertEqual(self.inventory.product.name, "Laptop")
        self.assertEqual(self.inventory.quantity, 4)
        self.assertEqual(str(self.inventory), "Inventory for Laptop")


