from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.db.models import QuerySet

from basket.models import ProductInBasket
from favorite.models import Favorite
from orders.models import Order
from shop.models import Reviews
from users.models import EmailForNews
from users.models import User


def update_user_in_basket(old_user: str, new_user: str) -> None:
    """
    Changes user authenticated to the email of the user in the shopping cart
    """
    ProductInBasket.objects.filter(user_authenticated=old_user).update(
        user_authenticated=new_user)


def update_user_in_favorite(old_user: str, new_user: str) -> None:
    """
    Changes user authenticated to the email of the user in the favorites
    """
    Favorite.objects.filter(user_authenticated=old_user).update(
        user_authenticated=new_user)


def add_email_to_the_mailing_list(email: str) -> EmailForNews:
    """
    Adds an email to the news mailing list
    """
    return EmailForNews.objects.create(email=email)


def get_email_from_email_the_news(email: str) -> EmailForNews:
    """
    Gets email from EmailForNews
    """
    return EmailForNews.objects.get(email=email)


def get_user_orders(request: WSGIRequest) -> QuerySet:
    """
    Returns a QuerySet of processed user orders.
    The user is received from request
    """
    user = request.user
    orders = Order.objects.filter(Q(user=user) | Q(email=user.email)).order_by('-id')
    return orders


def get_user(pk: int) -> User:
    """
    Gets a user by pk
    """
    return User.objects.get(pk=pk)


def get_user_reviews(request: WSGIRequest) -> QuerySet:
    """
    Returns a QuerySet of processed user reviews.
    The user is received from request
    """
    return Reviews.objects.filter(user=request.user)
