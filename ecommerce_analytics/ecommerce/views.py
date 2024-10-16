from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Inventory, Customer
from .serializers import InventorySerializer, CustomerSerializer, ProductSerializer

from datetime import datetime

class SalesDataView(APIView):
    permission_classes= [IsAuthenticated]

    def get(self, request):
        print("hi")
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not start_date or not end_date:
            return Response({"error": "Please provide a start and end date."}, status=status.HTTP_400_BAD_REQUEST)

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        sales_analytics = SalesAnalytics(start_date, end_date)
        revenue_by_category = sales_analytics.calculate_revenue_by_category()
        return Response(revenue_by_category)

class InventoryUpdateView(APIView):
    permission_classes= [IsAuthenticated]

    def post(self, request, pk):
        print("hi")
        try:
            print(pk)
            inventory = Inventory.objects.get(pk=pk)
            print(pk)
        except Inventory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = InventorySerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.http import HttpResponse
from openpyxl import Workbook
class ExportSalesReportView(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self, request):
        sales_analytics = SalesAnalytics(datetime.now().replace(day=1), datetime.now())
        report_data = sales_analytics.calculate_revenue_by_category()
        wb = Workbook()
        ws = wb.active
        ws.title = "Monthly Sales Report"
        ws.append(['Category', 'Revenue'])
        for item in report_data:
            ws.append([item['product__category__name'], item['revenue']])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="sales_report.xlsx"'
        wb.save(response)
        return response

class CustomerInfoView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from .models import OrderItem, Customer  
from ecommerce.services.sales_analytics import SalesAnalytics  
from datetime import timedelta
from ecommerce.services.sales_analytics import SalesAnalytics
from ecommerce.services.recommendation_engine import RecommendationEngine

def sales_analytics_view(request):
    start_date = request.GET.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    analytics = SalesAnalytics(start_date, end_date)
    revenue_by_category = analytics.calculate_revenue_by_category()
    top_selling_products = analytics.top_selling_products_by_country()
    churn_rate = analytics.calculate_customer_churn_rate()
    data = {
        'revenue_by_category': list(revenue_by_category), 'top_selling_products': list(top_selling_products),'customer_churn_rate': churn_rate,
    }
    return JsonResponse(data)

class ProductRecommendationView(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            recommendation_engine = RecommendationEngine(customer)
            recommended_products = recommendation_engine.suggest_from_similar_customers()
            serializer = ProductSerializer(recommended_products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

from unittest.mock import patch

