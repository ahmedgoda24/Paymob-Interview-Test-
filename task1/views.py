from django.shortcuts import render

# Create your views here.
# views.py
from django.db.models import F, Count, Window
from django.db.models.functions import RowNumber
from rest_framework import viewsets,generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product ,Category
from .serializers import CategorySerializer, ProductSerializer
from .pagination import DefaultPagination




class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Product.objects.select_related('category').all().order_by('id')
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination


    @action(detail=False, methods=['get'], url_path='top_most_expensive_by_category')
    def top_most_expensive_by_category(self, request):
        """
        Retrieves the top 10 most expensive products per category.
        and Annotate each product with the total number of products in its category. 

        This method uses Django's ORM to annotate each product with its row number
        within its category, ordered by price in descending order. It also annotates
        each product with the total count of products in its category. Only the top
        10 products by price are selected per category.

        The results are paginated, and the response includes serialized data of the
        products with their respective categories and product count annotations.
        
        Returns:
            A paginated response containing serialized data of the top 10 most
            expensive products for each category.
        """

        products = Product.objects.annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=[F('category')],
                order_by=F('price').desc()
            ),
            category_product_count=Window(
                expression=Count('id'),
                partition_by=[F('category')]
            )
        ).filter(row_number__lte=10).select_related('category')
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='top_10_most_expensive')
    def top_10_most_expensive(self, request):
        products = (Product.objects.select_related('category').annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=[F('category')],
                order_by=F('price').desc()
            )
        ).filter(row_number__lte=10)
        .order_by('category__name', '-price')
        )

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['get'], url_path='products_with_category_counts')
    def products_with_category_counts(self, request):
        """
        Retrieves all products annotated with the total number of products in their category.

        This method uses Django's ORM to annotate each product with the total count of
        products in its category. The results are paginated, and the response includes
        serialized data of the products with their respective category and product count
        annotations.
        and we can also get this query from category by using
        Category.objects.annotate(category_product_count=Count('products')).all
        select_related('products')
        Returns:
            A paginated response containing serialized data of all products with their
            respective category and product count annotations.
        """
        products = Product.objects.annotate(
            category_product_count=Window(
                expression=Count('id'),
                partition_by=[F('category')],
                )
        ).select_related('category')
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


