from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Inventory, Customer
from .serializers import InventorySerializer, CustomerSerializer, ProductSerializer

from datetime import datetime

# API view to handle fetching sales data within a date range
class SalesDataView(APIView):
    permission_classes= [IsAuthenticated] # Requires authentication

    # Handles GET requests to retrieve sales data based on date range
    def get(self, request):
        print("hi")
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        # If either start or end date is missing, return an error
        if not start_date or not end_date:
            return Response({"error": "Please provide a start and end date."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert start and end dates from query parameters into datetime format
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # Perform sales analytics calculation for the given date range by calling the SalesAnalytics class
        sales_analytics = SalesAnalytics(start_date, end_date)
        revenue_by_category = sales_analytics.calculate_revenue_by_category()
        return Response(revenue_by_category)
    
# API view to handle inventory updates
class InventoryUpdateView(APIView):
    permission_classes= [IsAuthenticated]

    # Handles POST requests to update inventory by product ID
    def post(self, request, pk):
        print("hi")
        try:
            print(pk)
            inventory = Inventory.objects.get(pk=pk) # Retrieve the inventory id
            print(pk)
        except Inventory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) # Return 404 if inventory not found
        # Serialize the incoming data for inventory update
        serializer = InventorySerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save() # Save the updated inventory
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.http import HttpResponse
from openpyxl import Workbook
class ExportSalesReportView(APIView):
    #permission_classes = [IsAuthenticated]
    # Handles GET requests to generate a sales report and export it as an Excel file
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        sales_analytics = SalesAnalytics(start_date, end_date)
        report_data = sales_analytics.calculate_revenue_by_category()
        print(report_data)
        # Create an Excel workbook and populate it with sales data
        wb = Workbook()
        ws = wb.active
        ws.title = "Monthly Sales Report"
        ws.append(['Category', 'Revenue'])
        for item in report_data:
            ws.append([item['product__category__name'], item['revenue']]) # Append sales data to Excel sheet

        # Prepare the response to return the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="sales_report.xlsx"'
        wb.save(response)  # Save the workbook to the response
        return response

# API view to retrieve customer information
class CustomerInfoView(APIView):
    permission_classes= [IsAuthenticated]
    # Handles GET requests to fetch customer details by ID
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk) # Retrieve customer 
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) # Return 404 if customer not found
        serializer = CustomerSerializer(customer) # Serialize the customer data
        return Response(serializer.data)

    
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from .models import OrderItem, Customer  
from ecommerce.services.sales_analytics import SalesAnalytics  
from datetime import timedelta
from .services.sales_analytics import SalesAnalytics
from .services.recommendation_engine import RecommendationEngine

def sales_analytics_view(request):
    # Default to the last 30 days if no date range is provided
    start_date = request.GET.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', datetime.now().strftime('%Y-%m-%d'))

    # Parse the date range
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Perform sales analytics for the date range by calling the SalesAnalytics class
    analytics = SalesAnalytics(start_date, end_date)
    revenue_by_category = analytics.calculate_revenue_by_category()
    top_selling_products = analytics.top_selling_products_by_country()
    churn_rate = analytics.calculate_customer_churn_rate()
    # Return the analytics data in JSON format
    data = {
        'revenue_by_category': list(revenue_by_category), 'top_selling_products': list(top_selling_products),'customer_churn_rate': churn_rate,
    }
    return JsonResponse(data)

# API view for product recommendation based on customer data    
class ProductRecommendationView(APIView):
    # Handles GET requests to fetch product recommendations for a customer
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id) # Retrieve the customer
            recommendation_engine = RecommendationEngine(customer) #Call the Recommendation engine with customer
            recommended_products = recommendation_engine.suggest_from_similar_customers() # Get recommended products
            serializer = ProductSerializer(recommended_products, many=True) # Serialize the recommended products
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND) # Return 404 if customer not found

