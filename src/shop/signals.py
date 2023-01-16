from shop.tasks import update_product_rating


def rating_in_product_post_save(sender, instance, created=None, **kwargs) -> None:
    """
    Reacts to the change or addition of product reviews.
    Updates the average product rating and the number of reviews.
    """
    update_product_rating.delay(instance.product.pk)
