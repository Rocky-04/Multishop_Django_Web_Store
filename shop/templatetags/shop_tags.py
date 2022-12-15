import logging

from django import template
from django.core.paginator import Paginator
from django.db.models import QuerySet

from shop.models import Category
from shop.models import Manufacturer
from shop.services import get_filter_products
from shop.services import get_rating_html
from shop.services import get_review_for_user_and_product
from shop.services import get_tag_by_banner

register = template.Library()

logger = logging.getLogger(__name__)


@register.inclusion_tag('shop/inc/list_categories.html')
def show_category(parent: int = None):
    """
    Shows subcategories
    """
    return {'category': Category.get_parent_categories(parent=parent)}


@register.inclusion_tag('shop/inc/banner.html')
def show_banner(pk_banner: int):
    """
    Shows banner from Tag
    """
    return {'tag': get_tag_by_banner(pk_banner)}


@register.inclusion_tag('shop/inc/carousel_banner.html')
def show_carousel_banner(pk_banner: int):
    """
    Shows carousel banner from Tag
    """
    return {'tag': get_tag_by_banner(pk_banner)}


@register.inclusion_tag('shop/inc/carousel_brand.html')
def show_carousel_brand():
    """
    Shows a carousel of brand logos with available products
    """
    return {'brand': Manufacturer.get_active_brand()}


@register.inclusion_tag('shop/inc/card_product.html', takes_context=True)
def show_card_product(context, item):
    """
    Shows a mini product card
    """
    return {'item': item,
            'PRODUCTS_FAVORITE_LIST': context['PRODUCTS_FAVORITE_LIST'],
            'PRODUCTS_BASKET_LIST': context['PRODUCTS_BASKET_LIST'],
            'request': context['request']
            }


@register.simple_tag()
def get_products(limit: int = 8, **kwargs) -> QuerySet:
    """
    Returns products with applied filters
    """
    return get_filter_products(limit=limit, **kwargs)


@register.simple_tag()
def get_all_categories():
    """
    Gets all categories
    """
    return Category.get_all_categories()


@register.simple_tag
def get_proper_elided_page_range(paginator, number, on_each_side=1, on_ends=1):
    """
    Returns the paginator
    """
    paginator = Paginator(paginator.object_list, paginator.per_page)
    return paginator.get_elided_page_range(number=number, on_each_side=on_each_side,
                                           on_ends=on_ends)


@register.simple_tag()
def get_user_review(user_id: int, product_id: int):
    """
    Returns the rating given by the user of the product
    """
    return get_review_for_user_and_product(user_id=user_id, product_id=product_id)


@register.simple_tag()
def get_fa_star(rating: int = 5) -> str:
    """
    Draws product rating stars based on average rating
    """
    return get_rating_html(rating)
