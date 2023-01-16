from orders.tasks import update_order_price


def product_in_order_post_save(sender, instance, created=None, **kwargs):
    """
    Update the order when changing products in the order, handling exceptions if necessary.

    This function retrieves all products in the order, then calculates the order total price and
    delivery cost based on the products and promo code (if applicable). It updates the order's
    delivery, total price, and promo code fields and saves the changes to the database.

    :param sender: The model class that sent the signal.
    :param instance: The instance of the model that triggered the signal.
    :param created: A boolean indicating whether the instance was just created.
    :param kwargs: Additional keyword arguments passed from the signal.
    :return: None
    """
    update_order_price.delay(instance.order.pk)
