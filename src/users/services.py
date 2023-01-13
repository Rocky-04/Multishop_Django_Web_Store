import logging

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.db.models import QuerySet

from basket.models import ProductInBasket
from favorite.models import Favorite
from orders.models import Order
from shop.models import Reviews
from users.models import EmailForNews
from users.models import User

logger = logging.getLogger(__name__)


def update_user_in_basket(old_user: str, new_user: str) -> None:
    """
    Update the user authenticated field in the shopping cart table handling exceptions if necessary.

    This function updates the `user_authenticated` field of all rows in the `ProductInBasket` table
    that match the given `old_user` value with the given `new_user` value.

    :param old_user: The current user authenticated value.
    :param new_user: The new user authenticated value.
    :return: None
    """
    try:
        ProductInBasket.objects.filter(user_authenticated=old_user).update(
            user_authenticated=new_user)
    except Exception as error:
        logger.error(f"Error updating user in shopping cart: {error}")


def update_user_in_favorite(old_user: str, new_user: str) -> None:
    """
    Update the user authenticated field in the favorites table, handling exceptions if necessary.

    This function updates the `user_authenticated` field of all rows in the `Favorite` table that
    match the given `old_user` value with the given `new_user` value.

    :param old_user: The current user authenticated value.
    :param new_user: The new user authenticated value.
    :return: None
    """
    try:
        Favorite.objects.filter(user_authenticated=old_user).update(
            user_authenticated=new_user)
    except Exception as error:
        logger.error(f"Error updating user in favorites: {error}")


def add_email_to_the_mailing_list(email: str) -> EmailForNews:
    """
    Add an email to the news mailing list, handling exceptions if necessary.

    This function adds the given `email` to the `EmailForNews` table. If the email already exists
    in the table, it raises a `EmailForNews.IntegrityError` exception.

    :param email: The email to add to the news mailing list.
    :return: The `EmailForNews` object that was created.
    :raises EmailForNews.IntegrityError: If the email already exists in the `EmailForNews` table.
    """
    try:
        return EmailForNews.objects.create(email=email)
    except EmailForNews.IntegrityError as error:
        logger.error(f"Email {email} already exists in the news mailing list: {error}")
        raise error
    except Exception as error:
        logger.error(f"Error adding email {email} to the news mailing list: {error}")
        raise error


def get_email_from_email_the_news(email: str) -> EmailForNews:
    """
    Get an email from the EmailForNews table, handling exceptions if necessary.

    This function retrieves an email from the `EmailForNews` table by its `email` field. If the
    email does not exist, it raises a `EmailForNews.DoesNotExist` exception.

    :param email: The email to retrieve from the `EmailForNews` table.
    :return: The `EmailForNews` object with the given email.
    :raises EmailForNews.DoesNotExist: If the email does not exist in the `EmailForNews` table.
    """
    try:
        return EmailForNews.objects.get(email=email)
    except EmailForNews.DoesNotExist as error:
        logger.error(f"Email {email} does not exist in EmailForNews: {error}")
        raise error
    except Exception as error:
        logger.error(f"Error getting email {email} from EmailForNews: {error}")
        raise error


def get_user_orders(request: WSGIRequest) -> QuerySet:
    """
    Get processed orders for a user, handling exceptions if necessary.

    :param request: The incoming request object.
    :return: A queryset of `Order` objects that belong to the user specified in the request.
    :raises ValueError: If the request does not have a `user` attribute.
    """
    try:
        user = request.user
        orders = Order.objects.filter(Q(user=user) | Q(email=user.email)).order_by('-id')
        return orders
    except ValueError as error:
        logger.error(f"Error getting user orders: {error}")
        raise error


def get_user(pk: int) -> User:
    """
    Get a user by primary key, handling exceptions if necessary.

    This function retrieves a user from the `User` table by its primary key `pk`. If the user does
    not exist, it raises a `User.DoesNotExist` exception.

    :param pk: The primary key of the user to retrieve.
    :return: The `User` object with the given primary key.
    :raises User.DoesNotExist: If the user with the given primary key does not exist.
    """
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist as error:
        logger.error(f"User with pk {pk} does not exist: {error}")
        raise error
    except Exception as error:
        logger.error(f"Error getting user with pk {pk}: {error}")
        raise error


def get_user_reviews(request: WSGIRequest) -> QuerySet:
    """
    Get processed reviews for a user, handling exceptions if necessary.

    This function returns a queryset of `Reviews` objects that belong to the user specified in the
    given `request` object. The user is determined from the request's `user` attribute. If the
    request does not have a `user` attribute, a `ValueError` is raised.

    :param request: The incoming request object.
    :return: A queryset of `Reviews` objects that belong to the user specified in the request.
    :raises ValueError: If the request does not have a `user` attribute.
    """
    try:
        return Reviews.objects.prefetch_related('product', 'product__default_varieties').filter(
            user=request.user)
    except ValueError as error:
        logger.error(f"Error getting user reviews: {error}")
        raise error
