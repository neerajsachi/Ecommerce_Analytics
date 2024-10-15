from ..models import OrderItem,Customer,Product

class RecommendationEngine:

    def __init__(self, customer):
        self.customer = customer

    def suggest_from_order_history(self):
        ordered_products = OrderItem.objects.filter(order__customer=self.customer).values_list('product', flat=True)
        ordered_categories = Product.objects.filter(id__in=ordered_products).values_list('category', flat=True)
        return Product.objects.filter(category__in=ordered_categories).exclude(id__in=ordered_products).distinct()
    
    def suggest_from_similar_customers(self):
        ordered_products = OrderItem.objects.filter(order__customer=self.customer).values_list('product', flat=True)
        similar_customers = Customer.objects.filter(orders__items__product__in=ordered_products).exclude(id=self.customer.id).distinct()
        return Product.objects.filter(orderitem__order__customer__in=similar_customers).exclude(orderitem__order__customer=self.customer).distinct()

    def suggest_based_on_inventory(self):
        return Product.objects.filter(inventory__quantity__gt=0).order_by('-inventory__quantity')
