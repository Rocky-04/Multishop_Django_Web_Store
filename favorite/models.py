from django.db import models

from shop.models import AttributeColor
from shop.models import AttributeSize
from shop.models import Product


class Favorite(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True,
                                   default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True,
                                null=True, default=None)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=0,
                                         default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    color = models.ForeignKey(AttributeColor, on_delete=models.CASCADE,
                              blank=True, null=True, default=None)
    size = models.ForeignKey(AttributeSize, on_delete=models.CASCADE,
                             blank=True, null=True, default=None)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
