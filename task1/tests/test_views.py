# import pytest
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from task1.models import Category, Product
# from decimal import Decimal

# @pytest.fixture
# def api_client():
#     return APIClient()

# @pytest.fixture
# def create_categories():
#     categories = [
#         Category.objects.create(name="Electronics"),
#         Category.objects.create(name="Clothing"),
#         Category.objects.create(name="Books")
#     ]
#     return categories

# @pytest.fixture
# def create_products(create_categories):
#     products = []
#     # Create products with different prices for each category
#     for category in create_categories:
#         for i in range(15):  # Create 15 products per category
#             price = Decimal('100.00') + (i * Decimal('10.00'))
#             product = Product.objects.create(
#                 name=f"{category.name} Product {i}",
#                 description=f"Description for {category.name} Product {i}",
#                 price=price,
#                 category=category
#             )
#             products.append(product)
#     return products

# @pytest.mark.django_db
# class TestProductViewSet:
#     def test_list_products(self, api_client, create_products):
#         url = reverse('product-list')
#         response = api_client.get(url)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert 'results' in response.data
#         assert len(response.data['results']) > 0

#     def test_top_most_expensive_by_category(self, api_client, create_products):
#         url = reverse('product-top-most-expensive-by-category')
#         response = api_client.get(url)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert 'results' in response.data
        
#         # Check that we get at most 10 products per category
#         category_counts = {}
#         for product in response.data['results']:
#             category_name = product['category']['name']
#             category_counts[category_name] = category_counts.get(category_name, 0) + 1
#             assert category_counts[category_name] <= 10
            
#             # Verify that products are ordered by price in descending order
#             if category_name in category_counts and category_counts[category_name] > 1:
#                 prev_product = response.data['results'][len(response.data['results'])-2]
#                 assert Decimal(product['price']) <= Decimal(prev_product['price'])

#     def test_top_10_most_expensive(self, api_client, create_products):
#         url = reverse('product-top-10-most-expensive')
#         response = api_client.get(url)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert 'results' in response.data
        
#         # Check that we get at most 10 products per category
#         category_counts = {}
#         for product in response.data['results']:
#             category_name = product['category']['name']
#             category_counts[category_name] = category_counts.get(category_name, 0) + 1
#             assert category_counts[category_name] <= 10

#     def test_products_with_category_counts(self, api_client, create_products):
#         url = reverse('product-products-with-category-counts')
#         response = api_client.get(url)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert 'results' in response.data
        
#         # Verify that each product has a category_product_count
#         for product in response.data['results']:
#             assert 'category_product_count' in product
#             # Since we created 15 products per category
#             assert product['category_product_count'] == 15

#     def test_pagination(self, api_client, create_products):
#         url = reverse('product-list')
#         response = api_client.get(url)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert 'count' in response.data
#         assert 'next' in response.data
#         assert 'previous' in response.data
#         assert 'results' in response.data
        
#         # Test next page
#         if response.data['next']:
#             next_response = api_client.get(response.data['next'])
#             assert next_response.status_code == status.HTTP_200_OK
#             assert len(next_response.data['results']) > 0 
#####################################################################################
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


# import pytest
# from rest_framework.test import APIClient
# from task1.factories import CategoryFactory, ProductFactory

# @pytest.mark.django_db
# def test_top_most_expensive_by_category_returns_max_10_per_category():
#     client = APIClient()

#     # Create 2 categories with 20 products each
#     for _ in range(2):
#         category = CategoryFactory()
#         ProductFactory.create_batch(20, category=category)

#     response = client.get("/api/products/top_most_expensive_by_category/")

#     assert response.status_code == 200
#     assert "results" in response.data
#     # Should return 10 from each category => 20 total
#     assert len(response.data["results"]) == 20


# @pytest.mark.django_db
# def test_top_10_most_expensive_returns_sorted_top_10():
#     client = APIClient()

#     category = CategoryFactory()
#     ProductFactory.create_batch(30, category=category)

#     response = client.get("/api/products/top_10_most_expensive/")

#     assert response.status_code == 200
#     assert "results" in response.data
#     results = response.data["results"]
#     assert len(results) <= 10

#     # Check if products are ordered by descending price
#     prices = [float(product["price"]) for product in results]
#     assert prices == sorted(prices, reverse=True)


# @pytest.mark.django_db
# def test_products_with_category_counts_has_category_product_count():
#     client = APIClient()

#     category = CategoryFactory()
#     ProductFactory.create_batch(15, category=category)

#     response = client.get("/api/products/products_with_category_counts/")

#     assert response.status_code == 200
#     assert "results" in response.data

#     for product in response.data["results"]:
#         assert "category_product_count" in product
#         assert product["category_product_count"] == 15
