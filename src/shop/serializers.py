from rest_framework import serializers

from shop.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'price', 'discount', 'price_now', 'description', 'category',
                  'rating']
