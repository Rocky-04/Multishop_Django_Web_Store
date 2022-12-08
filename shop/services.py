import logging
from typing import Union

from django.db.models import Count
from django.db.models import Q
from django.db.models import QuerySet
from modeltranslation.manager import MultilingualQuerySet

from shop.models import Banner
from shop.models import Color
from shop.models import Manufacturer
from shop.models import Product
from shop.models import Reviews
from shop.models import Size
from shop.models import Tag

logger = logging.getLogger(__name__)


def get_filter_products(limit: int = 8, **kwargs) -> QuerySet:
    """
     Returns products with applied filters
     """
    products = Product.objects.filter(**kwargs).order_by('-available', '-count_sale')[0:int(limit)]
    return products


def get_review(user_id: int, product_id: int) -> Union[Reviews, None]:
    """
    Returns the rating given by the user of the product
    """
    review = Reviews.objects.filter(user_id=user_id, product=product_id)
    if len(review) >= 1:
        return review[0]
    else:
        return None


def get_html_star(rating: int = 5) -> str:
    """
    Draws product rating stars based on average rating
    """
    rating = float(rating)
    star = ''

    for _ in range(5):
        if rating >= 0.5:
            star += '<i class="fas fa-star text-primary mr-1"></i>'
        elif rating > 0.3:
            star += '<i class="fas fa-star-half-alt text-primary mr-1"></i>'
        else:
            star += '<i class="far fa-star text-primary mr-1"></i>'
        rating -= 1
    return star


def get_tag(pk_banner: int) -> Tag:
    """
    Gets tags by pk_banner
    """
    try:
        tag = Tag.objects.get(title=Banner.objects.get(pk=pk_banner).tag)
    except Exception as error:
        logger.error(error)
        tag = Tag.objects.all().last()
    return tag


def get_color_filter(product_list_pk: list) -> MultilingualQuerySet:
    """
    Returns the MultilingualQuerySet of colors that are in product_list_pk
    """
    color_filter = Color.objects.annotate(cnt=Count('color__product', filter=Q(
        color__product__in=product_list_pk))).filter(cnt__gt=0).order_by('-cnt')

    return color_filter


def get_size_filter(product_list_pk: list) -> QuerySet:
    """
    Returns the MultilingualQuerySet of sizes that are in product_list_pk
    """
    size_filter = Size.objects.annotate(cnt=Count('size__product__product', filter=Q(
        size__product__product__in=product_list_pk))).filter(cnt__gt=0).order_by('-cnt')

    return size_filter


def get_manufacturer_filter(product_list_pk: list) -> QuerySet:
    """
    Returns the QuerySet of manufacturers that are in product_list_pk
    """
    manufacturer_filter = Manufacturer.objects.annotate(
        cnt=Count('manufacturer', filter=Q(manufacturer__in=product_list_pk))).filter(
        cnt__gt=0).order_by('-cnt')

    return manufacturer_filter
