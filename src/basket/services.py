import logging

from basket.models import ProductInBasket

logger = logging.getLogger(__name__)


def add_products_to_basket(user_authenticated: str,
                           product_id: int,
                           size_id: int,
                           color_id: int,
                           nmb: int = 1) -> None:
    """
    Adds a specified number of products to the user's basket. If the product
    is already in the basket, the quantity is updated.

    :param user_authenticated: The unique identifier of the session or user's email.
    :param product_id: The ID of the product to be added to the basket.
    :param size_id: The ID of the size of the product.
    :param color_id: The ID of the color of the product.
    :param nmb: The number of products to be added. Defaults to 1.
    """
    try:
        new_product, created = ProductInBasket.objects.get_or_create(
            user_authenticated=user_authenticated,
            product_id=product_id,
            size_id=size_id,
            color_id=color_id,
            defaults={"nmb": nmb})
        if not created:
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)
    except Exception as error:
        logger.error(f"Error adding products to basket {user_authenticated}: {error}")
        raise error


def remove_product_from_basket(user_authenticated: str,
                               product_id: int,
                               size_id: int,
                               color_id: int) -> None:
    """
    Removes a product from the basket of the given user.

    :param user_authenticated: The unique identifier of the session or user's email.
    :param product_id: The ID of the product to remove from the basket.
    :param size_id: The ID of the size of the product.
    :param color_id: The ID of the color of the product.
    """
    try:
        ProductInBasket.objects.get(user_authenticated=user_authenticated,
                                    product_id=product_id,
                                    size_id=size_id,
                                    color_id=color_id).delete()
    except Exception as error:
        logger.error(f"Error removing products to basket {user_authenticated}: {error}")
        raise error


def edit_product_from_basket(user_authenticated: str,
                             product_id: int,
                             size_id: int,
                             color_id: int,
                             nmb: int) -> None:
    """
    Updates the quantity of a product in the basket.

    :param user_authenticated: The unique identifier of the session or user's email.
    :param product_id: The ID of the product to update.
    :param size_id: The ID of the size of the product to update.
    :param color_id: The ID of the color of the product to update.
    :param nmb: The new quantity for the product.
    """
    try:
        new_product = ProductInBasket.objects.get(
            user_authenticated=user_authenticated,
            product_id=product_id,
            size_id=size_id,
            color_id=color_id)
        new_product.nmb = nmb
        new_product.save(force_update=True)
    except Exception as error:
        logger.error(f"Error editing products to basket {user_authenticated}: {error}")
        raise error


def get_basket_list(user_authenticated: str) -> tuple:
    """
    Retrieves the products in a user's basket and the number of products in a user's basket.

    :param user_authenticated: The unique identifier of the session or user's email.
    :return: A tuple containing:
            - A queryset of the products in the user's basket.
            - The number of products in the user's basket.
    """
    try:
        products = ProductInBasket.objects.filter(
            user_authenticated=user_authenticated,
            is_active=True).select_related(
            'size', 'color', 'product', 'product__default_varieties').values_list('size', flat=True)
        basket_nmb = len(products)
        return products, basket_nmb
    except Exception as error:
        logger.error(f"Error retrieving products in the basket {user_authenticated}: {error}")
        raise error
