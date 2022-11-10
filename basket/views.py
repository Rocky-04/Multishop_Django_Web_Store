from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from .models import ProductInBasket
from .ultis import BasketMixin


class BasketAddView(BasketMixin, View):
    """
    Adds products in the basket
    """

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        try:
            new_product, created = ProductInBasket.objects.get_or_create(
                session_key=self.session_key,
                product_id=self.product_id,
                is_active=True,
                size_id=self.size,
                color_id=self.color,
                defaults={"nmb": self.nmb})
            if not created:
                print("not created")
                new_product.nmb += int(self.nmb)
                new_product.save(force_update=True)

        except ValueError as err:
            return JsonResponse({'success': False, 'error': str(err)},
                                status=400)
        return HttpResponseRedirect(self.current)


class BasketRemoveView(BasketMixin, View):
    """
    Removes products in the basket
    """

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        try:
            ProductInBasket.objects.filter(session_key=self.session_key,
                                           product_id=self.product_id,
                                           size_id=self.size,
                                           color_id=self.color).delete()
        except ValueError as err:
            return JsonResponse({'success': False, 'error': str(err)},
                                status=400)
        return HttpResponseRedirect(self.current)


class ViewCart(BasketMixin, View):
    """
    Views products in the basket
    """

    template_name = 'basket/basket.html'

    def get(self, request):
        if request.user.is_authenticated:
            session_key = request.user.email
        else:
            session_key = request.session.session_key

        products_in_basket = ProductInBasket.objects.filter(
            session_key=session_key, is_active=True)

        context = {'title': 'Корзина',
                   'products_in_basket': products_in_basket,
                   }

        return render(request, self.template_name, context)


class EditCartView(BasketMixin, View):
    """
    Edits count products in the basket
    """

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        try:
            new_product = ProductInBasket.objects.get(
                session_key=self.session_key,
                product_id=self.product_id,
                size_id=self.size,
                color_id=self.color)
            new_product.nmb = self.nmb
            new_product.save(force_update=True)
        except ValueError as err:
            return JsonResponse({'success': False, 'error': str(err)},
                                status=400)

        return HttpResponseRedirect(self.current)
