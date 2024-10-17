from ..models import OrderItem,Customer,Product

class RecommendationEngine:

    def __init__(self, customer):
        # Initialize the class with a specific customer
        self.customer = customer

    def suggest_from_order_history(self):
        # Suggest products based on the customer's order history
        ordered_products = OrderItem.objects.filter(order__customer=self.customer).values_list('product', flat=True) #Get a list of product IDs the customer has previously ordered
        ordered_categories = Product.objects.filter(id__in=ordered_products).values_list('category', flat=True) # Get the categories of those ordered products
        return Product.objects.filter(category__in=ordered_categories).exclude(id__in=ordered_products).distinct() # Suggest products from the same categories but exclude already ordered products
    
    def suggest_from_similar_customers(self):
        # Suggest products based on similar customers' purchases
        ordered_products = OrderItem.objects.filter(order__customer=self.customer).values_list('product', flat=True)  # Find products that the customer has ordered
        similar_customers = Customer.objects.filter(orders__items__product__in=ordered_products).exclude(id=self.customer.id).distinct()  # Identify other customers who have ordered the same products (exclude the current customer)
        return Product.objects.filter(orderitem__order__customer__in=similar_customers).exclude(orderitem__order__customer=self.customer).distinct()  # Suggest products ordered by these similar customers that the current customer hasn't ordered

    def suggest_based_on_inventory(self):
        # Suggest products that are currently in stock, ordered by the highest available quantity
        return Product.objects.filter(inventory__quantity__gt=0).order_by('-inventory__quantity')
