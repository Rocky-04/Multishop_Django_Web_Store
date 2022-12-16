from django import template

from basket.models import ProductInBasket
from shop.models import Delivery

register = template.Library()


@register.inclusion_tag('basket/order_cost.html', takes_context=True)
def calculate_order_cost(context, show_button=False):
    """
    Calculates the cost of the products in the user's basket and the delivery cost for the order.

    :param context: The context for the template in which the tag is being used.
    :param show_button: A boolean indicating whether to show a button in the template.
            Defaults to False.
    :return: A dictionary containing the following keys:
        - 'request': The request object for the current request.
        - 'products_in_basket': A queryset of the products in the user's basket.
        - 'amount': The total cost of the products in the user's basket.
        - 'delivery': The delivery cost for the order.
        - 'button': The value of the `show_button` parameter.
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
            'button': show_button,
            }
