# serializers.py
from rest_framework import serializers
from .models import Product, Category

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name']

# class ProductSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     category_count = serializers.IntegerField(read_only=True)

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'price', 'category', 'created_at', 'category_count']
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    category_product_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'category', 
            'price', 
            'created_at',
            'category_product_count'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = representation['category']['name']
        return representation