from django.contrib import admin

from favorite.models import Favorite


@admin.register(Favorite)
class ProductsFromFavorite(admin.ModelAdmin):
    list_display = [field.name for field in Favorite._meta.fields]
