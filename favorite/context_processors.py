from .models import Favorite


def add_favorites(request):
    """
    Creates a list of the user's products in the favorite.
    Creates a variable for the number of items in the favorite.
    """
    user_authenticated = request.session['user_authenticated']
    products = Favorite.get_products_in_user_favorite(user_authenticated)
    favorite_nmb = products.count()
    favorite_list = products.values_list('size', flat=True)
    return {
        'PRODUCTS_FAVORITE_NMB': favorite_nmb,
        'PRODUCTS_FAVORITE_LIST': favorite_list,
    }
