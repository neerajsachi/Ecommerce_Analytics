
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

#product category model
class Category(models.Model):
    name = models.CharField(max_length=100) #category name

    def __str__(self):
        return self.name

#Tag model
class Tag(models.Model):
    name = models.CharField(max_length=100) #name of tag

    def __str__(self):
        return self.name

#custom manager for frequently used projects
class frequently_used_product_manager(models.Manager):
    def available_products(self):
        return self.filter(inventory__quantity__gt=0)

#product model  
class Product(models.Model):
    name = models.CharField(max_length=100) #product name
    description = models.TextField() #product description
    SKU = models.CharField(max_length=100, unique=True) #product SKU
    price = models.DecimalField(max_digits=20, decimal_places=2) #product price
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) #product category
    tags = models.ManyToManyField(Tag, related_name='products') #product tag

    frequently_used_products = frequently_used_product_manager() #custom manager
    objects = models.Manager() #Default manager

    def __str__(self):
        return self.name
    
from django.utils import timezone

#customer model
class Customer(models.Model):
    name = models.CharField(max_length=100) #customer name
    email = models.EmailField(unique=True) #customer email
    country = models.CharField(max_length=100) #customer country
    registration_date = models.DateTimeField(default=timezone.now) #customer registration data

    def __str__(self):
        return self.name

    #calculate customer life time value based on all their orders
    def lifetime_value(self):
        return sum(order.total_amount for order in self.orders.all())
    
#Order model
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE) #customer who placed the order
    order_date = models.DateTimeField(default=timezone.now) #order date 
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING') #Status of order
    total_amount = models.DecimalField(max_digits=10, decimal_places=2) #total amount of order

    def __str__(self):
        return f"Order {self.id} for {self.customer.name}" # String representation of the order 

    def calculate_tax(self):
        country_tax_rates = {'US': 0.07,'UK': 0.20,'IN': 0.18} #Tax rates for US,UK,India

        default_tax_rate = 0.05
        tax_rate = country_tax_rates.get(self.customer.country, default_tax_rate) #calculate country specific tax rates
        return self.total_amount * tax_rate

#Model representing the item ordered
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE) #the order for which the item belongs
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #product being ordered
    quantity = models.PositiveIntegerField() #quantity of product ordered
    price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2) #price at the time of order

    def __str__(self):
        return f"{self.quantity} of {self.product.name}" # String representation of the order item

# Signal receiver to update inventory when an order item is saved
@receiver(post_save, sender=OrderItem)
def update_inventory(sender, instance, **kwargs):
    inventory = instance.product.inventory # Get the product's inventory
    print("hi8")
    if inventory.quantity >= instance.quantity:
        print("hi1")
        inventory.quantity -= instance.quantity # Deduct ordered quantity from inventory
        inventory.save() # Save the updated inventory
    else:
        raise ValueError("Not enough stock to fulfill the order.") # Raise error if stock is insufficient

#Inventory model
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE) # One-to-one relationship with the product
    quantity = models.PositiveIntegerField() # Quantity available in stock
    last_restocked_date = models.DateTimeField() # Date when product was last restocked

    def __str__(self):
        return f"Inventory for {self.product.name}" # String representation of the inventory

     # Override save method to display a restock alert when quantity is low
    def save(self, *args, **kwargs):
        if self.quantity < 5:  
            print(f"Restock alert: {self.product.name} is low on stock!")
        super().save(*args, **kwargs)
