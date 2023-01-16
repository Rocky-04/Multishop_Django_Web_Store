from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        from django.db.models.signals import post_save
        from django.db.models.signals import post_delete
        from orders.models import GoodsInTheOrder
        from orders.signals import product_in_order_post_save

        post_save.connect(product_in_order_post_save, sender=GoodsInTheOrder)
        post_delete.connect(product_in_order_post_save, sender=GoodsInTheOrder)
