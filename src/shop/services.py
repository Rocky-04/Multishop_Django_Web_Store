import logging
from typing import List
from typing import Optional
from typing import Union

from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
from django.db.models import Count
from django.db.models import Q
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
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
    Retrieves a queryset of products that match the specified filters.

    :param limit: The maximum number of products to return (defaults to 99999)
    :param kwargs: Filters to apply to the products queryset (e.g. category="Clothing")
    :return: A QuerySet of matching products
    """
    return Product.objects.filter(**kwargs).prefetch_related('default_varieties').order_by(
        '-available', '-count_sale')[0:int(limit)]


def get_review_for_user_and_product(user_id: int, product_id: int) -> Optional[Reviews]:
    """
    Retrieves the review (if any) that the specified user has left for the specified product.

    :param user_id: The ID of the user to retrieve the review for.
    :param product_id: The ID of the product to retrieve the review for.
    :return: The review for the specified user and product, or None if no review exists.
    """
    try:
        review = Reviews.objects.get(user_id=user_id, product_id=product_id)
        return review
    except Reviews.DoesNotExist:
        return None


def get_rating_html(rating: int = 5) -> str:
    """
    Draws product rating stars based on average rating.

    :param rating: The average rating of the product, on a scale of 1 to 5.
    :return: A string containing the HTML for the star rating.
    """
    rating = float(rating)
    html_stars = ""

    # Loop 5 times to create the 5 stars
    for _x in range(5):
        if rating >= 0.5:
            html_stars += '<i class="fas fa-star text-primary mr-1"></i>'
        elif rating > 0.3:
            html_stars += '<i class="fas fa-star-half-alt text-primary mr-1"></i>'
        else:
            html_stars += '<i class="far fa-star text-primary mr-1"></i>'
        rating -= 1

    # Return the HTML for the star rating
    return html_stars


def get_tag_by_banner(pk_banner: int) -> Tag:
    """
    Gets the tag for a given banner. If no banner with the given primary key exists, return the
    last tag in the database as a default.

    :param pk_banner: The primary key of the banner.
    :return:  The tag for the given banner.
    """
    try:
        # Get the tag for the banner with the given primary key
        tag = Tag.objects.get(title=Banner.objects.get(pk=pk_banner).tag)
    except Exception as error:
        logger.error(error)

        # Return the last tag in the database as a default
        tag = Tag.objects.all().last()

    return tag


def filter_colors_by_products(product_list_pk: list) -> MultilingualQuerySet:
    """
    Gets the color filter for a list of products.

    :param product_list_pk: The primary keys of the products to filter.
    :return: A queryset of colors that are associated with the given products,
        ordered by the number of times each color appears in the product list.
    """
    color_filter = Color.objects.annotate(cnt=Count('color__product', filter=Q(
        color__product__in=product_list_pk))).filter(cnt__gt=0).order_by('-cnt')

    return color_filter


def filter_size_by_products(product_list_pk: list) -> QuerySet:
    """
    Gets the size filter for a list of products.

    :param product_list_pk: The primary keys of the products to filter.
    :return: A queryset of size that are associated with the given products,
        ordered by the number of times each size appears in the product list.
    """

    size_filter = Size.objects.annotate(cnt=Count('size__product__product', filter=Q(
        size__product__product__in=product_list_pk))).filter(cnt__gt=0).order_by('-cnt')

    return size_filter


def filter_manufacturers_by_products(product_list_pk: list) -> QuerySet:
    """
    Gets the manufacturer filter for a list of products.

    :param product_list_pk: The primary keys of the products to filter.
    :return: A queryset of manufacturers that are associated with the given products,
        ordered by the number of times each manufacturer appears in the product list.
    """
    manufacturer_filter = Manufacturer.objects.annotate(
        cnt=Count('manufacturer', filter=Q(manufacturer__in=product_list_pk))).filter(
        cnt__gt=0).order_by('-cnt')

    return manufacturer_filter


def convert_str_to_int_list(string_of_numbers: str) -> list:
    """
    Converts a string of numbers in list format to a list of integers.

    :param string_of_numbers: The string to convert, in the format '[25, 14, 13, 20]'.
    :return: A list of integers that were extracted from the input string.
    """
    number_list = [int(i) for i in string_of_numbers[1:-1].split(', ')]

    return number_list


def get_product_ids(data: Union[str, QuerySet, None] = '') -> list:
    """
    Forms a list of product identifiers based on the given data.

    :param data: The data to use to generate the list of product identifiers.
            This can be a string of numbers in list format, a queryset of products,
            or None to use all products in the database.
    :return: A list of product identifiers.
    """
    # If data is a string, convert it to a list of integers
    if data and isinstance(data, str):
        return convert_str_to_int_list(data)

    # If data is a queryset, return a list of primary keys for the products in the queryset
    if isinstance(data, (QuerySet, MultilingualQuerySet)):
        return list(data.values_list('pk', flat=True))

    # If data is None or an empty string, return a list of primary keys
    # for all products in the database
    if data is None or data == '':
        return list(Product.objects.all().values_list('pk', flat=True))

    # If data is of an invalid type, log an error and raise a TypeError
    logger.error(f'Invalid type data. Type: {type(data)}')
    raise TypeError


def get_filtered_products_by_color(color: list) -> QuerySet:
    """
    Gets the products that match the given color filter.
    If no color filter is specified, get all products.

    :param color: A list of colors to filter by.
    :return: A queryset of products that match the given color filter.
    """
    if color:
        products = AttributeColor.objects.filter(
            Q(color__in=color)).values_list('product', flat=True)
    else:
        products = AttributeColor.objects.all().values_list('product', flat=True)
    return products


def get_filtered_products_by_size(size: list) -> QuerySet:
    """
    Gets the products that match the given size filter.
    If no size filter is specified, get all products.

    :param size: A list of size to filter by.
    :return: A queryset of products that match the given size filter.
    """
    if size:
        products = AttributeSize.objects.filter(
            Q(size__in=size)).values_list('product__product', flat=True)
    else:
        products = AttributeSize.objects.all().values_list('product__product', flat=True)
    return products


def get_filtered_products_by_manufacturer(brand: list) -> QuerySet:
    """
    Gets the products that match the given brand filter.
    If no brand filter is specified, get all products.

    :param brand: A list of brand to filter by.
    :return: A queryset of products that match the given manufacturer filter.
    """
    if brand:
        products = Manufacturer.objects.filter(
            Q(id__in=brand)).values_list('manufacturer', flat=True)
    else:
        products = Manufacturer.objects.all().values_list('manufacturer', flat=True)
    return products


def apply_product_filters(request: WSGIRequest, pk_list: list) -> QuerySet:
    """
    Filters a list of products based on criteria specified in a WSGIRequest object.
    The function filters the product list using criteria such as minimum and maximum price,
    color, size, and manufacturer.

    :param request: A WSGIRequest object containing the criteria to use for filtering
        the product list.
    :param pk_list: The list of product primary keys to filter.
    :return: A QuerySet object containing a filtered list of products.
    """

    # Get the minimum and maximum price filter values from the request object
    min_price = request.GET.get('min_price') or 0
    max_price = request.GET.get('max_price') or 100000

    # Get the filtered products by color, size, and manufacturer
    filter_color = get_filtered_products_by_color(request.GET.getlist("color"))
    filter_size = get_filtered_products_by_size(request.GET.getlist("size"))
    filter_manufacturer = get_filtered_products_by_manufacturer(request.GET.getlist("manufacturer"))

    # Filter the product list using the given criteria
    queryset = Product.objects.filter(
        Q(pk__in=pk_list) & Q
        (pk__in=filter_color) & Q
        (pk__in=filter_size) & Q
        (pk__in=filter_manufacturer) & Q
        (price_now__gte=min_price,
         price_now__lte=max_price)
    )

    # Return the filtered product list
    return queryset


def get_nested_category_ids(category_slug: str) -> List[int]:
    """
    Gets a list of primary keys for the given category and its nested subcategories.

    :param category_slug: The slug of the category to get the nested subcategories for.
    :return: A list of primary keys for the given category and its nested subcategories.
    """
    category = Category.objects.get(slug=category_slug)
    categories = category.get_descendants(include_self=True)
    return list(categories.values_list('pk', flat=True))


def send_contact_form_message(request: WSGIRequest) -> None:
    """
    Sends a message from a user using a contact form on a website.

    :param request: A WSGIRequest object containing the message to send.
    :return: None.
    """

    data = request.POST
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    # Check if all required fields are filled in
    if not all([name, email, subject, message]):
        # Show an error message if any required fields are missing
        messages.error(request,
                       _('Error sending the letter. Please fill in all the required fields.'))
        logger.warning('Error sending the letter: missing required fields')
        return

    # Compose the email subject and message
    text_subject = f"contact form: {subject} {name}"
    text_message = (f"You have received a new message from your website contact form.\n\n"
                    f"Here are the details:\n\nName: {name}\n\n\nEmail: {email}\n\n"
                    f"Subject: {subject}\n\nMessage: {message}")

    # Send the email and show a success or error message
    mail = send_mail(text_subject, text_message, EMAIL_HOST_USER,
                     [email], fail_silently=False)
    if mail:
        messages.success(request, _('Thank you for your request'))
    else:
        messages.error(request,
                       _('Error sending the letter. Try again later'))
        logger.warning('Error sending the letter')


def get_product_active_color(product: Product, color: Union[str, None]) -> AttributeColor:
    """
    Gets the active color for a given product.

    :param product: The product to get the active color for.
    :param color: The color to get (if provided).
    :return: The active color for the given product.
    """

    if color is not None:
        color = product.attribute_color.get(color_id=color)
    elif product.available:
        color = product.get_color()[0]
    else:
        color = AttributeColor.objects.filter(product=product)[0]
    return color


def get_product_active_size(active_color: AttributeColor, size: Union[str, None]) -> AttributeSize:
    """
    Gets the active size for a given product.

    :param active_color: The active product color to get the active size for.
    :param size: The size to get (if provided).
    :return: The active size for the given product color.
    """
    if size is not None:
        size = active_color.attribute_size.get(size_id=size)
    elif active_color.available:
        size = active_color.get_size()[0]
    else:
        size = active_color.get_size(available=False)[0]
    return size


def add_or_update_review(form: ReviewsForm, request: WSGIRequest) -> None:
    """
    Adds a product review if the form is valid and the user is authenticated.
    If the authenticated user has already left a review for the given product,
    the existing review is updated with the new values provided in the form.
    Otherwise, a new review is created.

    :param form: The ReviewsForm object containing the review data.
    :param request: The WSGIRequest object representing the user's request.
    :return: None.
    """

    # Check if the form is valid and the user is authenticated
    if form.is_valid() and request.user.is_authenticated:
        # Get the review text and rating from the form
        text = form.data['text']
        rating = form.data['rating']
        user = request.user
        product_id = request.POST.get('product_id')

        # Check if the user has already left a review for the product
        review, created = Reviews.objects.get_or_create(
            user=user, product_id=product_id,
            defaults={"text": text, "rating": rating}
        )

        # If the user has already left a review, update the review with the new values
        if not created:
            review.text = text
            review.rating = rating
            review.save()

        # Show a success message
        messages.success(request, _('Feedback successfully left'))
    else:
        # Show an error message
        messages.error(request, _('Failed to leave feedback. Try again later'))
        logger.warning('Failed to leave feedback')


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    """
    A custom filter that combines the functionality of the `BaseInFilter` and `CharFilter
    """
    pass


class ProductFilter(filters.FilterSet):
    """
    Filters the product by the selected attributes.

    Available filters:
        - price_now: The price of the product, specified as a range.
        - rating: The rating of the product, specified as a range.
        - count_reviews: The number of reviews for the product, specified as a range.
        - available: A boolean filter indicating whether the product is available.
        - discount: The discount applied to the product, specified as a range.
        - category: The category of the product, specified as a list of category slugs.
        - manufacturer: The manufacturer of the product, specified as a list of manufacturer slugs.
        - country: The country of origin for the product, specified as a list of country slugs.
        - tags: The tags associated with the product, specified as a list of tag slugs.
    """
    price_now = filters.RangeFilter()
    rating = filters.RangeFilter()
    count_reviews = filters.RangeFilter()
    available = filters.BooleanFilter()
    discount = filters.RangeFilter()
    category = CharFilterInFilter(field_name='category__slug', lookup_expr='in')
    manufacturer = CharFilterInFilter(field_name='manufacturer__slug', lookup_expr='in')
    country = CharFilterInFilter(field_name='country__slug', lookup_expr='in')
    tags = CharFilterInFilter(field_name='tags__slug', lookup_expr='in')

    class Meta:
        model = Product
        fields = ['price_now', 'available', 'discount', 'category', 'manufacturer', 'country',
                  'tags', 'rating', 'count_reviews']
