from .services import get_basket_list


def basket(request):
    """
    Creates a QuerySet of the user's products in the basket.
    Creates a variable for the number of items in the basket.
    """
    user_authenticated = request.session['user_authenticated']
    basket_list, basket_nmb = get_basket_list(user_authenticated)
    return {
        'PRODUCTS_BASKET_NMB': basket_nmb,
        'PRODUCTS_BASKET_LIST': basket_list,
    }
