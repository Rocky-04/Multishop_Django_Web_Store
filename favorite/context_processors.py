from .models import Favorite


def add_favorites(request):
    """
    Creates a list of the user's products in the favorite.
    Creates a variable for the number of items in the favorite.
    """
    if request.user.is_authenticated:
        session_key = request.user.email
    else:
        session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    products = Favorite.objects.filter(session_key=session_key, is_active=True)
    favorite_total = products.count()
    favorite_list = products.values_list('size', flat=True)
    return locals()
