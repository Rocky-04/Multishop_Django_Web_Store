from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView

from basket.models import ProductInBasket
from orders.forms import CreateOrderForm
from orders.models import PromoCode
from orders.services import add_products_to_the_order_list


class CheckoutView(CreateView):
    form_class = CreateOrderForm
    template_name = 'orders/checkout.html'
    success_url = 'create_order/'

    def form_valid(self, form):
        """
        Checks the correctness of the order.
        Makes an order.
        Removes products from the shopping cart when the order is successfully created.
        """
        user_authenticated = self.request.session['user_authenticated']
        products_in_basket = ProductInBasket.get_products_from_user_basket(user_authenticated)
        if len(products_in_basket) > 0:
            self.object = form.save()
            if form.data['promo_code']:
                self.object.promo_code = PromoCode.get_promo_code(title=form.data['promo_code'])
            if self.request.user.is_authenticated:
                self.object.user = self.request.user
            self.object.save()
        else:
            messages.error(self.request, _('Empty basket. First you need to add a product'))
            return HttpResponseRedirect(self.request.path_info)

        add_products_to_the_order_list(products_in_basket, order_id=self.object.pk)

        return HttpResponseRedirect(self.get_success_url())


class CreateOrderView(View):
    template_name = 'orders/order_done.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
