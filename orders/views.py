from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView

from basket.models import ProductInBasket
from orders.forms import CreateOrderForm
from orders.models import GoodsInTheOrder
from orders.models import PromoCode


class CheckoutView(CreateView):
    form_class = CreateOrderForm
    template_name = 'orders/checkout.html'
    success_url = 'create_order/'

    def form_valid(self, form):
        """
        Checks the correctness of the order.
        Makes an order.
        Removes products from the shopping cart when the order is successful.
        """
        user_authenticated = self.request.session['user_authenticated']
        products_in_basket = ProductInBasket.objects.filter(user_authenticated=user_authenticated)
        if len(products_in_basket) > 0:
            self.object = form.save()
            if form.data['promo_code']:
                promo_code = PromoCode.objects.get(title=form.data['promo_code'])
                self.object.promo_code = promo_code
            if self.request.user.is_authenticated:
                self.object.user = self.request.user
        else:
            messages.error(self.request, _('Empty basket. First you need to add a product'))
            return HttpResponseRedirect(self.request.path_info)

        for item in products_in_basket:
            GoodsInTheOrder.objects.create(product=item.product,
                                           order=self.object,
                                           total_price=item.total_price,
                                           nmb=item.nmb,
                                           price_per_item=item.price_per_item,
                                           color=item.color,
                                           size=item.size)
            item.product.count_sale += 1
            item.product.save()
            item.delete()
        return HttpResponseRedirect(self.get_success_url())


class CreateOrderView(View):
    template_name = 'orders/order_done.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
