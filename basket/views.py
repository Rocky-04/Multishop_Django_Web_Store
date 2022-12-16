from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from .models import ProductInBasket
from .services import add_products_to_basket
from .services import edit_product_from_basket
from .services import remove_product_from_basket
from .ultis import BasketMixin


class ViewCart(BasketMixin, View):
    """
    Views products in a user's basket
    """
    template_name = 'basket/basket.html'

    def get(self, request):
        user_authenticated = request.session['user_authenticated']
        products_in_basket = ProductInBasket.get_products_from_user_basket(user_authenticated)
        context = {'title': _('Product basket'),
                   'products_in_basket': products_in_basket}

        return render(request, self.template_name, context)


class BasketAddView(BasketMixin, View):
    """
    Adds a specified number of products to the user's basket. If the product
    is already in the basket, the quantity is updated.
    """

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        add_products_to_basket(
            user_authenticated=self.user_authenticated,
            product_id=self.product_id,
            size_id=self.size,
            color_id=self.color,
            nmb=self.nmb)

        return HttpResponseRedirect(self.current)


class BasketRemoveView(BasketMixin, View):
    """
    Removes a product from the basket of the given user.
    """

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        remove_product_from_basket(
            user_authenticated=self.user_authenticated,
            product_id=self.product_id,
            size_id=self.size,
            color_id=self.color)

        return HttpResponseRedirect(self.current)


class EditCartView(BasketMixin, View):
    """
    Updates the quantity of a product in the basket.
    """

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        edit_product_from_basket(
            user_authenticated=self.user_authenticated,
            product_id=self.product_id,
            size_id=self.size,
            color_id=self.color,
            nmb=self.nmb)

        return HttpResponseRedirect(self.current)
