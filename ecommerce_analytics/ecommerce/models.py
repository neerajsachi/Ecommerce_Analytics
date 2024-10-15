
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class frequently_used_product_manager(models.Manager):
    def available_products(self):
        return self.filter(inventory__quantity__gt=0)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    SKU = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, related_name='products')

    frequently_used_products = frequently_used_product_manager()
    objects = models.Manager()

    def __str__(self):
        return self.name
    
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def lifetime_value(self):
        return sum(order.total_amount for order in self.orders.all())

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} for {self.customer.name}"

    def calculate_tax(self):
        country_tax_rates = {'US': 0.07,'UK': 0.20,'IN': 0.18}

        default_tax_rate = 0.05
        tax_rate = country_tax_rates.get(self.customer.country, default_tax_rate)
        return self.total_amount * tax_rate

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

@receiver(post_save, sender=OrderItem)
def update_inventory(sender, instance, **kwargs):
    inventory = instance.product.inventory
    print("hi8")
    if inventory.quantity >= instance.quantity:
        print("hi1")
        inventory.quantity -= instance.quantity
        inventory.save()
    else:
        raise ValueError("Not enough stock to fulfill the order.")

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    last_restocked_date = models.DateTimeField()

    def __str__(self):
        return f"Inventory for {self.product.name}"

    def save(self, *args, **kwargs):
        if self.quantity < 5:  
            print(f"Restock alert: {self.product.name} is low on stock!")
        super().save(*args, **kwargs)
