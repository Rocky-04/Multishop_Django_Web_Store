from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
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
                user_authenticated=self.user_authenticated,
                product_id=self.product_id,
                is_active=True,
                size_id=self.size,
                color_id=self.color,
                defaults={"nmb": self.nmb})
            if not created:
                new_product.nmb += int(self.nmb)
                new_product.save(force_update=True)

        except ValueError as err:
            print(err)
            messages.error(request, _(
                'An error occurred during the execution of the action. Try again later'))
        return HttpResponseRedirect(self.current)


class BasketRemoveView(BasketMixin, View):
    """
    Removes products in the basket
    """

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        try:
            ProductInBasket.objects.filter(user_authenticated=self.user_authenticated,
                                           product_id=self.product_id,
                                           size_id=self.size,
                                           color_id=self.color).delete()
        except ValueError as err:
            print(err)
            messages.error(request, _(
                'An error occurred during the execution of the action. Try again later'))
        return HttpResponseRedirect(self.current)


class ViewCart(BasketMixin, View):
    """
    Views products in the basket
    """

    template_name = 'basket/basket.html'

    def get(self, request):
        user_authenticated = request.session['user_authenticated']
        products_in_basket = ProductInBasket.get_products_in_user_basket(user_authenticated)
        context = {'title': _('Product basket'),
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
                user_authenticated=self.user_authenticated,
                product_id=self.product_id,
                size_id=self.size,
                color_id=self.color)
            new_product.nmb = self.nmb
            new_product.save(force_update=True)
        except ValueError as err:
            print(err)
            messages.error(request, _(
                'An error occurred during the execution of the action. Try again later'))

        return HttpResponseRedirect(self.current)
