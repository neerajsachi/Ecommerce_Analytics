from django.db.models import Sum, Count, F
from datetime import datetime, timedelta
from ..models import OrderItem,Customer

class SalesAnalytics:

    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date
    def calculate_revenue_by_category(self):
        return (OrderItem.objects.filter(order__order_date__range=[self.start_date, self.end_date]).values('product__category__name').annotate(revenue=Sum(F('quantity') * F('price_at_time_of_order'))).order_by('-revenue'))

    def top_selling_products_by_country(self):
        return (OrderItem.objects.filter(order__order_date__range=[self.start_date, self.end_date]).values('order__customer__country', 'product__name').annotate(total_sales=Sum('quantity')).order_by('-total_sales'))

    def calculate_customer_churn_rate(self):
        # churn is defined as no orders in the last 6 months
        six_months_ago = datetime.now() - timedelta(days=6 * 30)
        total_customers = Customer.objects.count()
        active_customers = Customer.objects.filter(orders__order_date__gte=six_months_ago).distinct().count()
        churned_customers = total_customers - active_customers
        churn_rate = churned_customers / total_customers if total_customers > 0 else 0
        return churn_rate
