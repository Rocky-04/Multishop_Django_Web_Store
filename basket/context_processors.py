from .models import ProductInBasket


def basket(request):
    """
    Creates a QuerySet of the user's products in the basket.
    Creates a variable for the number of items in the basket.
    """
    user_authenticated = request.session['user_authenticated']
    products = ProductInBasket.get_products_in_user_basket(user_authenticated)
    products_basket_nmb = products.count()
    products_basket_list = products.values_list('size', flat=True)
    return {
        'PRODUCTS_BASKET_NMB': products_basket_nmb,
        'PRODUCTS_BASKET_LIST': products_basket_list,
    }
