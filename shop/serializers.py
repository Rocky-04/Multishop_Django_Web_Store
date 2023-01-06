from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from shop.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'price', 'description', 'category', 'rating']
        depth = 1



