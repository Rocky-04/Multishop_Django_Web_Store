from favorite.models import Favorite
import logging

logger = logging.getLogger(__name__)


def add_products_to_favorites(product_id: int,
                              size_id: int,
                              color_id: int,
                              user_authenticated: str
                              ) -> None:
    """
    Adds a product to the user's favorites.

    :param product_id: The ID of the product to add to the favorites.
    :param size_id: The ID of the size of the product to add to the favorites.
    :param color_id: The ID of the color of the product to add to the favorites.
    :param user_authenticated: The unique identifier of the session or user's email.
    :return: None
    """
    try:
        Favorite.objects.get_or_create(user_authenticated=user_authenticated,
                                       product_id=product_id,
                                       size_id=size_id,
                                       color_id=color_id)
    except Exception as error:
        logger.error(f"Error adding product to favorites for user {user_authenticated}: {error}")
        raise error


def remove_products_from_favorites(product_id: int,
                                   size_id: int,
                                   color_id: int,
                                   user_authenticated: str
                                   ) -> None:
    """
    Removes a product from the user's favorites.

    :param product_id: The ID of the product to remove from the favorites.
    :param size_id: The ID of the size of the product to remove from the favorites.
    :param color_id: The ID of the color of the product to remove from the favorites.
    :param user_authenticated: The unique identifier of the session or user's email.
    :return: None
    """
    try:
        Favorite.objects.filter(user_authenticated=user_authenticated,
                                product_id=product_id,
                                size_id=size_id,
                                color_id=color_id).delete()
    except Exception as error:
        logger.error(
            f"Error removing product from favorites for user {user_authenticated}: {error}")
        raise error


def get_favorite_list(user_authenticated: str) -> tuple:
    """
    Creates a QuerySet of the user's products in the favorite and a variable for the number of items
        in the favorite.

    :param user_authenticated: The unique identifier of the session or user's email.
    :return: A tuple containing the QuerySet of favorite products and the number of items
        in the favorite.
    """
    try:
        products = Favorite.get_products_user_from_favorite(user_authenticated)
        favorite_list = products.values_list('size', flat=True)
        favorite_nmb = products.count()
        return favorite_list, favorite_nmb
    except Exception as error:
        logger.error(f"Error retrieving favorite products for user {user_authenticated}: {error}")
        return (), 0