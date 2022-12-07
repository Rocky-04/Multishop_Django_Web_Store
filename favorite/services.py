from favorite.models import Favorite


def add_products_to_favorites(product_id: int,
                              size_id: int,
                              color_id: int,
                              user_authenticated: str
                              ) -> None:
    """
    Adds products from the favorite
    """

    Favorite.objects.get_or_create(user_authenticated=user_authenticated,
                                   product_id=product_id,
                                   size_id=size_id,
                                   color_id=color_id)


def remove_products_from_favorites(product_id: int,
                                   size_id: int,
                                   color_id: int,
                                   user_authenticated: str
                                   ) -> None:
    """
    Removes products from the favorite
    """

    Favorite.objects.filter(user_authenticated=user_authenticated,
                            product_id=product_id,
                            size_id=size_id,
                            color_id=color_id).delete()


def get_favorite_list(user_authenticated: str) -> tuple:
    """
    Creates a QuerySet of the user's products in the favorite.
    favorite_list: QuerySet
    Creates a variable for the number of items in the favorite.
    favorite_nmb: int
    """
    products = Favorite.get_products_user_from_favorite(user_authenticated)
    favorite_list = products.values_list('size', flat=True)
    favorite_nmb = products.count()
    return favorite_list, favorite_nmb
