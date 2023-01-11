import logging
from decimal import Decimal

from django.db import models
from django.db.models import QuerySet
from django.db.models import Sum

from shop.models import AttributeColor
from shop.models import AttributeSize
from shop.models import Product

logger = logging.getLogger(__name__)


class ProductInBasket(models.Model):
    user_authenticated = models.CharField(max_length=128, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True,
                                default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    color = models.ForeignKey(AttributeColor, on_delete=models.CASCADE, blank=True, null=True,
                              default=None)
    size = models.ForeignKey(AttributeSize, on_delete=models.CASCADE, blank=True, null=True,
                             default=None)

    class Meta:
        verbose_name = 'Products in the basket'
        verbose_name_plural = 'Products in the basket'

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs) -> None:
        """
        Saves the product price and the price based on the quantity product to the database.

        :param args: Additional arguments to be passed to the parent class's save method.
        :param kwargs: Additional keyword arguments to be passed to the parent class's save method.
        :return: None
        """
        price_per_item = self.product.price_now
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item
        super(ProductInBasket, self).save(*args, **kwargs)

    @staticmethod
    def get_amount_from_user_basket(user_authenticated: str) -> Decimal:
        """
        Calculates the total cost of goods in the basket for the specified user.

        :param user_authenticated: The username of the user to retrieve the basket amount for.
        :return: The total cost of goods in the user's basket, or 0 if there are no items
            in the basket.
        """
        try:
            basket_total = ProductInBasket.objects.filter(
                user_authenticated=user_authenticated,
                size__available=True).aggregate(
                total=Sum('total_price'))['total']
            return 0 if basket_total is None else basket_total
        except Exception as error:
            logger.error(f"Error calculating basket total for user {user_authenticated}: {error}")
            return 0

    @staticmethod
    def get_products_from_user_basket(user_authenticated: str) -> QuerySet:
        """
        Returns the products in the basket for the specified user.

        :param user_authenticated: The username of the user to retrieve the basket products for.
        :return: A queryset of `ProductInBasket` objects representing the products in the user's
            basket, or an empty queryset if an error occurs.
        """
        try:
            return ProductInBasket.objects.filter(user_authenticated=user_authenticated,
                                                  is_active=True)
        except Exception as error:
            logger.error(f"Error retrieving basket products for user {user_authenticated}: {error}")
            return ProductInBasket.objects.none()
