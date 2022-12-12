import logging
from typing import Union

from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
from django.db.models import Count
from django.db.models import Q
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from modeltranslation.manager import MultilingualQuerySet

from online_store.settings import EMAIL_HOST_USER
from shop.forms import ReviewsForm
from shop.models import AttributeColor
from shop.models import AttributeSize
from shop.models import Banner
from shop.models import Category
from shop.models import Color
from shop.models import Manufacturer
from shop.models import Product
from shop.models import Reviews
from shop.models import Size
from shop.models import Tag

logger = logging.getLogger(__name__)


def get_filter_products(limit: int = 99999, **kwargs) -> QuerySet:
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

    for _x in range(5):
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


def convert_str_into_list_int(string_of_numbers: str) -> list:
    """
    Converts a string ('[25, 14, 13, 20]') into a list of numbers
    """
    return [int(i) for i in string_of_numbers[1:-1].split(', ')]


def get_products_list_pk(data: Union[str, QuerySet, None] = '') -> list:
    """
    Forms a list of product identifiers
    """
    if data and isinstance(data, str):
        return convert_str_into_list_int(data)
    if isinstance(data, (QuerySet, MultilingualQuerySet)):
        return list(data.values_list('pk', flat=True))
    if data is None or data == '':
        return list(Product.objects.all().values_list('pk', flat=True))
    logger.error(f'Invalid type data. Type: {type(data)}')
    raise TypeError


def get_products_with_color_filtered(color: list) -> QuerySet:
    """
    Filters the product by selected colors
    """
    if color:
        filter_color = AttributeColor.objects.filter(
            Q(color__in=color)).values_list('product', flat=True)
    else:
        filter_color = AttributeColor.objects.all().values_list('product', flat=True)
    return filter_color


def get_products_with_size_filtered(size: list) -> QuerySet:
    """
    Filters the product by selected sizes
    """
    if size:
        filter_size = AttributeSize.objects.filter(
            Q(size__in=size)).values_list('product__product', flat=True)
    else:
        filter_size = AttributeSize.objects.all().values_list(
            'product__product', flat=True)
    return filter_size


def get_products_with_manufacturer_filtered(manufacturer: list) -> QuerySet:
    """
    Filters the product by selected manufacturers
    """
    if manufacturer:
        filter_manufacturer = Manufacturer.objects.filter(
            Q(id__in=manufacturer)).values_list('manufacturer', flat=True)
    else:
        filter_manufacturer = Manufacturer.objects.all().values_list('manufacturer', flat=True)
    return filter_manufacturer


def filter_products(request: WSGIRequest, product_list_pk: list) -> QuerySet:
    """
    Filters the product by the selected attributes
    Available filters: min_price, max_price, color, size, manufacturer
    """
    if request.GET.get('min_price'):
        min_price = request.GET.get('min_price')
    else:
        min_price = 0
    if request.GET.get('max_price'):
        max_price = request.GET.get('max_price')
    else:
        max_price = 100000

    filter_color = get_products_with_color_filtered(request.GET.getlist("color"))
    filter_size = get_products_with_size_filtered(request.GET.getlist("size"))
    filter_manufacturer = get_products_with_manufacturer_filtered(
        request.GET.getlist("manufacturer"))

    queryset = Product.objects.filter(
        Q(pk__in=product_list_pk) & Q
        (pk__in=filter_color) & Q
        (pk__in=filter_size) & Q
        (pk__in=filter_manufacturer) & Q
        (price_now__gte=min_price,
         price_now__lte=max_price)
    )
    return queryset


def get_list_of_nested_category_id(slug: str) -> list:
    """
    Returns a list of nested categories id by category slug
    """
    categories = Category.objects.get(slug=slug).get_descendants(include_self=True)
    return list(categories.values_list('pk', flat=True))


def send_message_from_user(request: WSGIRequest) -> None:
    """
    Sends a message from the user to the email
    """
    data = request.POST
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    if name and email and subject and message:
        text_subject = f"contact form: {subject} {name}"
        text_message = (f"You have received a new message from your website contact form.\n\n"
                        f"Here are the details:\n\nName: {name}\n\n\nEmail: {email}\n\n"
                        f"Subject: {subject}\n\nMessage: {message}")
        mail = send_mail(text_subject, text_message, EMAIL_HOST_USER,
                         [email], fail_silently=False)
        if mail:
            messages.success(request, _('Thank you for your request'))
        else:
            messages.error(request,
                           _('Error sending the letter. Try again later'))
            logger.warning('Error sending the letter')
    else:
        messages.error(request,
                       _('Error sending the letter. Try again later'))
        logger.warning('Error sending the letter')


def get_active_color(product: Product, color: Union[str, None]) -> AttributeColor:
    """
    Gets active AttributeColor selected product.
    If active_color is not selected returns main AttributeColor.
    """
    if color is not None:
        color = product.attribute_color.get(color_id=color)
    elif product.available:
        color = product.get_color()[0]
    else:
        color = AttributeColor.objects.filter(product=product)[0]
    return color


def get_active_size(active_color: AttributeColor, size: Union[str, None]) -> AttributeSize:
    """
    Gets active AttributeSize selected product.
    If active_size is not selected returns main AttributeSize.
    """
    if size is not None:
        size = active_color.attribute_size.get(size_id=size)
    elif active_color.available:
        size = active_color.get_size()[0]
    else:
        size = active_color.get_size(available=False)[0]
    return size


def add_user_review(form: ReviewsForm, request: WSGIRequest) -> None:
    """
    If form valid and user is authenticated, adds a product review.
    """
    if form.is_valid() and request.user.is_authenticated:
        text = form.data['text']
        rating = form.data['rating']
        user = request.user
        product_id = request.POST.get('product_id')

        review = Reviews.objects.filter(user=user, product=product_id)

        if len(review) >= 1:
            review.update(text=text,
                          rating=rating)
        else:
            Reviews.objects.create(user=user,
                                   product_id=product_id,
                                   text=text,
                                   rating=rating)
        messages.success(request, _('Feedback successfully left'))
    else:
        messages.error(request, _('Failed to leave feedback. Try again later'))
        logger.warning('Failed to leave feedback')
