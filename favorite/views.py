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
        user_authenticated = request.session['user_authenticated']

        data = request.POST
        size = data.get("size")
        color = data.get("color")
        product_id = kwargs.get('id')
        current = request.POST.get('current')

        try:
            Favorite.objects.get_or_create(user_authenticated=user_authenticated,
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
        user_authenticated = request.session['user_authenticated']

        data = request.POST
        size = data.get("size")
        color = data.get("color")
        product_id = kwargs.get('id')
        current = request.POST.get('current')

        try:
            Favorite.objects.filter(user_authenticated=user_authenticated,
                                    product_id=product_id,
                                    is_active=True, size_id=size,
                                    color_id=color).delete()
        except ValueError as err:
            return JsonResponse({'success': False, 'error': str(err)},
                                status=400)
        return HttpResponseRedirect(current)


class FavoriteView(View):
    """
    Views products in the favorite
    """

    def get(self, request):
        user_authenticated = request.session['user_authenticated']
        favorites = Favorite.objects.filter(user_authenticated=user_authenticated)
        context = {'favorites': favorites}
        return render(request, 'favorite/favorite.html', context=context)
