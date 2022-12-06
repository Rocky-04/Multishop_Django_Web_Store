import logging

from basket.models import ProductInBasket

logger = logging.getLogger(__name__)


def add_products_to_basket(user_authenticated: str,
                           product_id: int,
                           size_id: int,
                           color_id: int,
                           nmb: int = 1) -> None:
    """
    Adds products to the basket, if the product is already
     in the basket, totals the quantity
    """
    new_product, created = ProductInBasket.objects.get_or_create(
        user_authenticated=user_authenticated,
        product_id=product_id,
        size_id=size_id,
        color_id=color_id,
        defaults={"nmb": nmb})
    if not created:
        new_product.nmb += int(nmb)
        new_product.save(force_update=True)


def remove_product_from_basket(user_authenticated: str,
                               product_id: int,
                               size_id: int,
                               color_id: int) -> None:
    """
    Removes products from the basket
    """
    ProductInBasket.objects.get(user_authenticated=user_authenticated,
                                product_id=product_id,
                                size_id=size_id,
                                color_id=color_id).delete()


def edit_product_from_basket(user_authenticated: str,
                             product_id: int,
                             size_id: int,
                             color_id: int,
                             nmb: int) -> None:
    """
    Edits count products from the basket
    """
    new_product = ProductInBasket.objects.get(
        user_authenticated=user_authenticated,
        product_id=product_id,
        size_id=size_id,
        color_id=color_id)
    new_product.nmb = nmb
    new_product.save(force_update=True)
