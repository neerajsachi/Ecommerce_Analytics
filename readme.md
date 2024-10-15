###
Introduction
This project is an E-Commerce Analytics Platform designed to provide insights into sales data, customer behavior, and product performance. The platform utilizes Django REST Framework to expose APIs for front-end consumption and analytics processing.

###
Prerequisites:

1.Python 3.8 or higher
2.Django 3.2 or higher
3.Django REST Framework
4.MySQL Database
5.Virtual Environment (optional but recommended)
6.openpyxl

###
Steps:
1.Clone the Repository:git clone https://github.com/neerajsachi/Ecommerce_Analytics/
cd ecommerce-analytics

2.Create a Virtual Environment

3.Install Dependencies: pip install -r requirements.txt

4.Set Up Database:

    Create a MySQL database for your project.
    Update the DATABASES section in settings.py to point to your MySQL database.

5.Run Migrations:python manage.py migrate

6.Create a superuser: python manage.py createsuperuser

7.Run the development server: python manage.py runserver

####
Key Design Decisions

    1.Django and Django REST Framework:
        Chosen for their robust features and ease of use for building APIs. This choice allows for rapid development and clear separation of concerns between the front-end and back-end.

    2.MySQL as the Database:
        MySQL was selected for its reliability and performance in handling complex queries. It provides the necessary structure to efficiently manage relational data, which is crucial for analytics.

    3.Class-Based Views (CBVs):
        Implemented CBVs for API endpoints to facilitate better organization of the code and promote reuse of common logic. This approach improves readability and maintainability.

    4.Modular Architecture:
        The project follows a modular architecture to separate concerns and improve scalability. Each app (e.g., orders, customers) encapsulates related functionality, making the project easier to manage and extend.

    5.API Documentation with drf-yasg:
        Integrated drf-yasg for automatic API documentation generation. This enhances developer experience and provides clear documentation for API consumers.

###
Advanced Business Logic

Revenue Calculations

The application implements sophisticated revenue calculations to provide insights into sales performance across different categories. This includes:

    Total Revenue by Category: Calculated by aggregating sales data and summing the revenue generated for each product category. This helps in identifying high-performing categories and strategizing inventory management.

    Top-Selling Products: A feature that identifies products with the highest sales volume, facilitating targeted marketing efforts and inventory restocking decisions.

Customer Churn Analysis

The project incorporates a customer churn rate analysis, which is essential for understanding customer retention. This is calculated by:

    Tracking the number of customers who make purchases over a specific period versus the total number of customers.
    Providing insights into customer behavior and assisting in developing retention strategies.

Recommendation Engine

The application includes a recommendation engine that suggests products based on order history. This business logic utilizes:

    Collaborative Filtering: Analyzing the purchasing patterns of similar customers to suggest products that other customers with similar preferences have bought.
    Order History Analysis: Leveraging previous purchases to enhance customer experience and increase sales through personalized suggestions.

Modular and Scalable Architecture

The project is designed with a modular architecture, allowing for easy addition of new features and applications without disrupting existing functionalities. This architecture:

    Separates Concerns: Each module (e.g., customers, orders) handles its own logic, making the codebase more maintainable.
    Supports Scalability: The architecture is designed to handle increased data loads and new features as the business grows.
###
API Documentation:

    The API documentation is generated automatically and can be accessed at http://127.0.0.1:8000/swagger/ once the server is running.