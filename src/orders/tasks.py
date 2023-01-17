import logging

from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction

from orders.models import GoodsInTheOrder, Order
from shop.models import Delivery

logger = logging.getLogger(__name__)


@shared_task(base=Singleton)
def update_order_price(order_pk: int) -> None:
    """
    Update the order when changing products in the order, handling exceptions if necessary.

    This function retrieves all products in the order, then calculates the order total price and
    delivery cost based on the products and promo code (if applicable). It updates the order's
    delivery, total price, and promo code fields and saves the changes to the database.

    :param order_pk: The primary key of the order.
    """
    try:
        with transaction.atomic():
            order = Order.objects.get(pk=order_pk)
            all_products_in_order = GoodsInTheOrder.objects.filter(order=order)
            promo_code = 0
            order_total_price = 0
            for item in all_products_in_order:
                order_total_price += item.total_price
            if order_total_price:
                delivery = Delivery.get_delivery(order_total_price)
                order.delivery = delivery
                delivery = delivery.price
                if order.promo_code:
                    promo_code = order.promo_code.price
            else:
                order.delivery = None
                delivery = 0
            total_price = order_total_price + delivery - promo_code
            order.total_price = 0 if total_price < 0 else total_price
            order.save(force_update=True)
    except Exception as error:
        logger.error(f"Error updating order: {error}")
