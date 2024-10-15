from django.urls import path
from .views import SalesDataView, InventoryUpdateView, ExportSalesReportView, CustomerInfoView,sales_analytics_view, ProductRecommendationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('sales/', SalesDataView.as_view(), name='sales-data'),
    path('inventory/<int:pk>/', InventoryUpdateView.as_view(), name='inventory-update'),
    path('export-sales/', ExportSalesReportView.as_view(), name='export-sales'),
    path('customer/<int:pk>/', CustomerInfoView.as_view(), name='customer-info'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('recommendation/<int:customer_id>/', ProductRecommendationView.as_view(), name='product-recommendations'),
    path('sales-analytics/', sales_analytics_view, name='sales_analytics'),
]
