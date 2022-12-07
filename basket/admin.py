from django.contrib import admin

from .models import ProductInBasket


@admin.register(ProductInBasket)
class ProductInBasketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInBasket._meta.fields]
