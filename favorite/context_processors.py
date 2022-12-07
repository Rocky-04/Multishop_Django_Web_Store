from .services import get_favorite_list


def favorite(request):
    """
    Creates a QuerySet of the user's products in the favorite.
    Creates a variable for the number of items in the favorite.
    """
    user_authenticated = request.session['user_authenticated']
    favorite_list, favorite_nmb = get_favorite_list(user_authenticated)

    return {
        'PRODUCTS_FAVORITE_NMB': favorite_nmb,
        'PRODUCTS_FAVORITE_LIST': favorite_list,
    }
