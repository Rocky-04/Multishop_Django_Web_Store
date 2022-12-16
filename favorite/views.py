from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from .models import Favorite
from .services import add_products_to_favorites
from .services import remove_products_from_favorites


class FavoriteView(View):
    """
    View to display a list of the user's favorite products.
    """
    template_name = 'favorite/favorite.html'

    def get(self, request):
        user_authenticated = request.session['user_authenticated']
        favorites = Favorite.get_products_user_from_favorite(user_authenticated)
        context = {'favorites': favorites}

        return render(request, self.template_name, context=context)


class FavoriteAddView(View):
    """
    View to handle the addition of a product from the user's favorite list.
    """

    def post(self, request, *args, **kwargs):
        data = request.POST
        current = request.POST.get('current')
        user_authenticated = request.session['user_authenticated']

        current = request.POST.get('current')
        add_products_to_favorites(product_id=kwargs.get('id'),
                                  size_id=data.get("size"),
                                  color_id=data.get("color"),
                                  user_authenticated=user_authenticated)

        return HttpResponseRedirect(current)


class FavoriteRemoveView(View):
    """
    View to handle the removal of a product from the user's favorite list.
    """

    def post(self, request, *args, **kwargs):
        data = request.POST
        current = request.POST.get('current')
        user_authenticated = request.session['user_authenticated']

        remove_products_from_favorites(product_id=kwargs.get('id'),
                                       size_id=data.get("size"),
                                       color_id=data.get("color"),
                                       user_authenticated=user_authenticated)

        return HttpResponseRedirect(current)
