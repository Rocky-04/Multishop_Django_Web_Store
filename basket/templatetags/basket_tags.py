from django import template

from basket.models import ProductInBasket
from shop.models import Delivery

register = template.Library()


@register.inclusion_tag('basket/order_cost.html', takes_context=True)
def order_cost(context, button=False):
    """
    Calculates the cost of the order and the cost of delivery
    """
    request = context['request']
    user_authenticated = request.session['user_authenticated']
    products_in_basket = ProductInBasket.get_products_from_user_basket(user_authenticated)
    amount = ProductInBasket.get_amount_from_user_basket(user_authenticated)
    delivery = Delivery.get_delivery(amount).price

    return {'request': request,
            'products_in_basket': products_in_basket,
            'amount': amount,
            'delivery': delivery,
            'button': button,
            }
