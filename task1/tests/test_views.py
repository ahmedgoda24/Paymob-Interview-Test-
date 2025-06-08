import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal
from task1.factories import CategoryFactory, ProductFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_products():
    categories = CategoryFactory.create_batch(3)
    products = []
    for category in categories:
        for i in range(15):
            products.append(ProductFactory(
                category=category,
                price=Decimal("100.00") + i * Decimal("10.00")
            ))
    return products
@pytest.mark.django_db
class TestProductViewSet:

    def test_list_products(self, api_client, create_products):
        url = reverse("product-list")
        response = api_client.get(url)
        assert response.status_code == 200
        assert 'results' in response.data
        assert len(response.data['results']) > 0

    @pytest.mark.parametrize("endpoint", [
        "product-top-most-expensive-by-category",
        "product-top-10-most-expensive",
        "product-products-with-category-counts"
    ])
    def test_custom_endpoints_respond_ok(self, api_client, create_products, endpoint):
        url = reverse(endpoint)
        response = api_client.get(url)
        assert response.status_code == 200
        assert 'results' in response.data

    def test_top_most_expensive_by_category_limits_to_10(self, api_client, create_products):
        url = reverse("product-top-most-expensive-by-category")
        response = api_client.get(url)
        data = response.data['results']
        
        # Debug print to see the actual data structure
        print("\nResponse data structure:")
        if data:
            print("First product:", data[0])
        
        category_counter = {}
        for product in data:
            # Handle both possible data structures
            category_name = product['category']['name'] if isinstance(product['category'], dict) else product['category']
            category_counter[category_name] = category_counter.get(category_name, 0) + 1
            assert category_counter[category_name] <= 10

    def test_top_10_most_expensive_sorted(self, api_client, create_products):
        url = reverse("product-top-10-most-expensive")
        response = api_client.get(url)
        prices = [Decimal(p['price']) for p in response.data['results']]
        assert prices == sorted(prices, reverse=True)

    def test_category_count_field_included(self, api_client, create_products):
        url = reverse("product-products-with-category-counts")
        response = api_client.get(url)
        for product in response.data['results']:
            assert 'category_product_count' in product
            assert product['category_product_count'] == 15

    def test_pagination_works(self, api_client, create_products):
        url = reverse("product-list")
        response = api_client.get(url)

        assert response.status_code == 200
        assert 'count' in response.data
        assert 'next' in response.data
        assert 'previous' in response.data
        assert 'results' in response.data

        if response.data['next']:
            next_url = response.data['next']
            next_response = api_client.get(next_url)
            assert next_response.status_code == 200
            assert len(next_response.data['results']) > 0

