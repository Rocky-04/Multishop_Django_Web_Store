import logging
from typing import List
from typing import Union

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
    Displays a list of subcategories for the specified parent category.

    :param parent: The ID of the parent category to retrieve subcategories for. If not specified,
            the top-level categories will be retrieved.
    :return: A dictionary containing the QuerySet of subcategories to be rendered in the template.
    """
    return {'category': Category.get_parent_categories(parent=parent)}


@register.inclusion_tag('shop/inc/banner.html')
def show_banner(pk_banner: int):
    """
    Displays a banner on the website using the specified tag.

    :param pk_banner: The ID of the tag that should be used to retrieve the banner.
    :return: A dictionary containing the tag to be rendered in the template.
    """
    return {'tag': get_tag_by_banner(pk_banner)}


@register.inclusion_tag('shop/inc/carousel_banner.html')
def show_carousel_banner(pk_banner: int):
    """
    Displays a carousel banner on the website using the specified tag.

    :param pk_banner: The ID of the tag that should be used to retrieve the banner.
    :return: A dictionary containing the tag to be rendered in the template.
    """
    return {'tag': get_tag_by_banner(pk_banner)}


@register.inclusion_tag('shop/inc/carousel_brand.html')
def show_carousel_brand():
    """
    Displays a carousel of brand logos with available products on the website.

    :return: A dictionary containing the list of active brands to be rendered in the template.
    """
    return {'brand': Manufacturer.get_active_brand()}


@register.inclusion_tag('shop/inc/card_product.html', takes_context=True)
def show_card_product(context, item):
    """
    Shows a mini product card.

    :param context: The context in which the tag is used, containing the necessary information to
        render the card.
    :param item: The product object to be displayed in the card.
    :return: dict: The context data to be used to render the product card.
    """
    return {'item': item,
            'PRODUCTS_FAVORITE_LIST': context['PRODUCTS_FAVORITE_LIST'],
            'PRODUCTS_BASKET_LIST': context['PRODUCTS_BASKET_LIST'],
            'request': context['request']
            }


@register.simple_tag()
def get_products(limit: int = 8, **kwargs) -> QuerySet:
    """
    Returns a QuerySet of products with applied filters.

    :param limit: The maximum number of products to return.
    :param kwargs: Filters to apply to the products.
    :return: A QuerySet of products with applied filters.
    """
    return get_filter_products(limit=limit, **kwargs)


@register.simple_tag()
def get_all_categories() -> QuerySet:
    """
    Returns a QuerySet of all categories.

    :return: A QuerySet of all categories.
    """
    return Category.get_all_categories()


@register.simple_tag
def get_proper_elided_page_range(paginator, number, on_each_side=1, on_ends=1) -> List[int]:
    """
    Returns a list of page numbers for the paginator, with ellipses to indicate
    hidden pages.

    :param paginator: The paginator object.
    :param number: The current page number.
    :param on_each_side: The number of page numbers to display on each side of the
        current page number.
    :param on_ends: The number of page numbers to display at the beginning and end
        of the page range.
    :return: A list of page numbers for the paginator.
    """
    paginator = Paginator(paginator.object_list, paginator.per_page)
    return paginator.get_elided_page_range(number=number, on_each_side=on_each_side,
                                           on_ends=on_ends)


@register.simple_tag()
def get_user_review(user_id: int, product_id: int) -> Union[None, int]:
    """
    Returns the rating given by the user for the product, or None if the user
    has not provided a rating for the product.

    :param user_id: The ID of the user.
    :param product_id: The ID of the user.
    :return: The rating given by the user for the product, or None if the user
             has not provided a rating for the product
    """
    return get_review_for_user_and_product(user_id=user_id, product_id=product_id)


@register.simple_tag()
def get_fa_star(rating: int = 5) -> str:
    """
    Returns the HTML for a star icon to display the rating.

    :param rating: The rating to display, from 0 to 5.
    :return: The HTML for a star icon to display the rating.
    """
    return get_rating_html(rating)
