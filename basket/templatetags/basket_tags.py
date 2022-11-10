from django import template
from django.db.models import Sum

from basket.models import ProductInBasket
from shop.models import Delivery

register = template.Library()


@register.inclusion_tag('basket/order_cost.html', takes_context=True)
def order_cost(context, button=False):
    request = context['request']
    if request.user.is_authenticated:
        session_key = request.user.email
    else:
        session_key = request.session.session_key

    products_in_basket = ProductInBasket.objects.filter(
        session_key=session_key, is_active=True)
    if len(products_in_basket) > 0:
        amount = ProductInBasket.objects.filter(session_key=session_key,
                                                size__available=True).aggregate(
            total=Sum('total_price'))
        amount = amount['total']
        delivery = Delivery.get_delivery(amount).price

    else:
        amount = 0
        delivery = 0

    return {'products_in_basket': products_in_basket,
            'request': request,
            'amount': amount,
            'delivery': delivery,
            'button': button,
            }
