from typing import Dict
from typing import Union

from django.db.models import QuerySet

from .services import get_favorite_list


def favorite_products_context(request) -> Dict[str, Union[int, QuerySet]]:
    """
    Creates a QuerySet of the user's products in the favorite and a variable
    for the number of items in the favorite.

    :param request: The HTTP request object.
    :return: A dictionary containing the number of favorite items and the QuerySet
        of favorite products.
    """
    user_authenticated = request.session['user_authenticated']
    favorite_list, favorite_nmb = get_favorite_list(user_authenticated)

    return {
        'PRODUCTS_FAVORITE_NMB': favorite_nmb,
        'PRODUCTS_FAVORITE_LIST': favorite_list,
    }
