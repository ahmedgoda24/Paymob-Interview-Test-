from locust import HttpUser, task, between
from random import choice

class ProductAPIUser(HttpUser):
    # Wait between 1 and 5 seconds between tasks
    wait_time = between(1, 5)
    
    def on_start(self):
        """Initialize any user-specific data here"""
        pass

    @task(3)  # Higher weight for listing products as it's more common
    def list_products(self):
        """Test the main product listing endpoint"""
        self.client.get("/api/v1/task1/products/")

    @task(2)
    def get_top_most_expensive_by_category(self):
        """Test the top most expensive products by category endpoint"""
        self.client.get("/api/v1/task1/products/top_most_expensive_by_category/")

    @task(2)
    def get_top_10_most_expensive(self):
        """Test the top 10 most expensive products endpoint"""
        self.client.get("/api/v1/task1/products/top_10_most_expensive/")

    @task(1)  # Lower weight for category counts as it's less frequently accessed
    def get_products_with_category_counts(self):
        """Test the products with category counts endpoint"""
        self.client.get("/api/v1/task1/products/products_with_category_counts/")

    @task(1)
    def test_pagination(self):
        """Test pagination by accessing different pages"""
        # First page
        response = self.client.get("/api/v1/task1/products/")
        if response.status_code == 200 and "next" in response.json():
            # If there's a next page, try to access it
            next_page = response.json()["next"]
            if next_page:
                self.client.get(next_page) 