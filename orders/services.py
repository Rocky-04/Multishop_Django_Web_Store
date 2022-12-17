import logging

from django.db.models import QuerySet

from orders.models import GoodsInTheOrder
from orders.models import Order

logger = logging.getLogger(__name__)


def add_products_to_the_order_list(products_in_basket: QuerySet, order_id: int) -> None:
    """
    Add products from a shopping cart to an order list and update the product's sale count.

    This function retrieves an order by its ID, then iterates over the items in the shopping cart.
    For each item, it creates a new `GoodsInTheOrder` object and associates it with the order.
    The function then increments the product's sale count by 1 and saves the changes to the
    database. Finally, the function removes the item from the shopping cart.

    :param products_in_basket: A queryset of items in the shopping cart.
    :param order_id: The ID of the order to which the products should be added.
    :return: None
    """
    try:
        order = Order.objects.get(pk=order_id)
        for item in products_in_basket:
            GoodsInTheOrder.objects.create(product=item.product,
                                           order=order,
                                           total_price=item.total_price,
                                           nmb=item.nmb,
                                           price_per_item=item.price_per_item,
                                           color=item.color,
                                           size=item.size)
            item.product.count_sale += 1
            item.product.save()
            item.delete()
    except Order.DoesNotExist as error:
        logger.error(f"Order with ID {order_id} does not exist: {error}")
    except Exception as error:
        logger.error(f"Error adding products to order list: {error}")
