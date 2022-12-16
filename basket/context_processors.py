from typing import Dict
from typing import Union

from django.db.models import QuerySet

from .services import get_basket_list


def basket_products_context(request) -> Dict[str, Union[int, QuerySet]]:
    """
    Creates a context variable containing a queryset of the user's products in the basket,
    as well as a variable for the number of items in the basket.

    :return: A dictionary containing the context variables 'PRODUCTS_BASKET_LIST'
            and 'PRODUCTS_BASKET_NMB'.
    """
    user_authenticated = request.session['user_authenticated']
    basket_list, basket_nmb = get_basket_list(user_authenticated)

    return {
        'PRODUCTS_BASKET_LIST': basket_list,
        'PRODUCTS_BASKET_NMB': basket_nmb,
    }
