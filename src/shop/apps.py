from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'shop'

    def ready(self):
        from django.db.models.signals import post_save
        from shop.models import Reviews
        from shop.signals import rating_in_product_post_save

        post_save.connect(rating_in_product_post_save, sender=Reviews)
