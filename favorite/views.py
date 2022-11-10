from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from .models import Favorite


class FavoriteAddView(View):
    """
    Adds products in the favorite
    """

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            session_key = request.user.email
        else:
            session_key = request.session.session_key

        data = request.POST
        size = data.get("size")
        color = data.get("color")
        product_id = kwargs.get('id')
        current = request.POST.get('current')

        try:
            Favorite.objects.get_or_create(session_key=session_key,
                                           product_id=product_id,
                                           is_active=True, size_id=size,
                                           color_id=color)
        except ValueError as err:
            return JsonResponse({'success': False, 'error': str(err)},
                                status=400)
        return HttpResponseRedirect(current)


class FavoriteRemoveView(View):
    """
    Removes products in the favorite
    """

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            session_key = request.user.email
        else:
            session_key = request.session.session_key

        data = request.POST
        size = data.get("size")
        color = data.get("color")
        product_id = kwargs.get('id')
        current = request.POST.get('current')

        try:
            Favorite.objects.filter(session_key=session_key,
                                    product_id=product_id,
                                    is_active=True, size_id=size,
                                    color_id=color).delete()
        except ValueError as err:
            return JsonResponse({'success': False, 'error': str(err)},
                                status=400)
        return HttpResponseRedirect(current)


class FavotiteView(View):
    """
    Views products in the favorite
    """

    def get(self, request):
        if request.user.is_authenticated:
            session_key = request.user.email
        else:
            session_key = request.session.session_key

        favorites = Favorite.objects.filter(session_key=session_key)
        context = {'favorites': favorites}
        return render(request, 'favorite/favorite.html', context=context)
