from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
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
        if self.request.user.is_authenticated:
            session_key = self.request.user.email
        else:
            session_key = self.request.session.session_key
        products_in_basket = ProductInBasket.objects.filter(
            session_key=session_key)
        if len(products_in_basket) > 0:
            self.object = form.save()
            if form.data['promo_code']:
                promo_code = PromoCode.objects.get(
                    title=form.data['promo_code'])
                self.object.promo_code = promo_code
            if self.request.user.is_authenticated:
                self.object.user = self.request.user

        else:
            return JsonResponse({'success': False, 'error': 'Empty basket'},
                                status=400)

        for item in products_in_basket:
            print(item)
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
