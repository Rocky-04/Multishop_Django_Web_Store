from django.db.models import QuerySet

from orders.models import GoodsInTheOrder
from orders.models import Order


def add_products_to_the_order_list(products_in_basket: QuerySet, order_id: int) -> None:
    """
    Adds products from the shopping cart to the order list.
    Removes products from the shopping cart and adds product's count_sale when the product is
    successfully created.
    """
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
