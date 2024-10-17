from django.urls import path
from .views import SalesDataView, InventoryUpdateView, ExportSalesReportView, CustomerInfoView,sales_analytics_view, ProductRecommendationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # URL for fetching sales data within a date range
    path('sales/', SalesDataView.as_view(), name='sales-data'),

    # URL for updating inventory based on a specific product
    path('inventory/<int:pk>/', InventoryUpdateView.as_view(), name='inventory-update'),

    # URL for exporting sales data into an Excel file
    path('export-sales/', ExportSalesReportView.as_view(), name='export-sales'),

    # URL for retrieving customer details 
    path('customer/<int:pk>/', CustomerInfoView.as_view(), name='customer-info'),

    # URL for obtaining JWT tokens (login)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # URL for obtaining JWT refresh tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URL for product recommendations based on customer ID
    path('recommendation/<int:customer_id>/', ProductRecommendationView.as_view(), name='product-recommendations'),

    # URL for viewing sales analytics
    path('sales-analytics/', sales_analytics_view, name='sales_analytics'),
]
