import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from shop.models import AttributeColor
from shop.models import AttributeSize
from shop.models import Delivery
from shop.models import Product
from users.models import User

logger = logging.getLogger(__name__)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, verbose_name=_('First name'))
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True)
    postcode = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    additional_information = models.TextField(max_length=300, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.ForeignKey('Status', default=1, on_delete=models.SET_NULL, blank=True,
                               null=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, blank=True, null=True,
                                 default=None)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, blank=True,
                                       null=True, default=None)
    promo_code = models.ForeignKey('PromoCode', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class GoodsInTheOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True,
                                default=None)
    color = models.ForeignKey(AttributeColor, on_delete=models.SET_NULL, blank=True, null=True,
                              default=None)
    size = models.ForeignKey(AttributeSize, on_delete=models.SET_NULL, blank=True, null=True,
                             default=None)
    order = models.ForeignKey(Order, related_name="goods_in_the_order", on_delete=models.CASCADE,
                              blank=True, null=True, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = _('Goods in the order')
        verbose_name_plural = _('Goods in the orders')

    def save(self, *args, **kwargs):
        """
        Save the product and update the price fields.

        This method updates the `price_per_item` field with the current price of the product and
        the `total_price` field with the total price based on the quantity of the product. It then
        saves the object to the database.

        :param args: Additional positional arguments passed to the parent class's save method.
        :param kwargs: Additional keyword arguments passed to the parent class's save method.
        :return: None
        """
        try:
            self.price_per_item = self.product.price_now
            self.total_price = self.nmb * self.price_per_item
            super(GoodsInTheOrder, self).save(*args, **kwargs)
        except Exception as error:
            logger.error(f"Error saving GoodsInTheOrder object: {error}")


class Status(models.Model):
    title = models.CharField(max_length=24, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')


class PaymentMethod(models.Model):
    title = models.CharField(max_length=24, blank=True)

    def __str__(self):
        return self.title


class PromoCode(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.price)

    @staticmethod
    def get_promo_code(title: str) -> 'PromoCode':
        """
        Get a promo code by its title, handling exceptions if necessary.

        :param title: The title of the promo code to retrieve.
        :return: The promo code object.
        :raises PromoCode.DoesNotExist: If the promo code with the given title does not exist.
        """
        try:
            return PromoCode.objects.get(title=title)
        except PromoCode.DoesNotExist as error:
            logger.error(f"Promo code with title {title} does not exist: {error}")
            raise error
        except Exception as error:
            logger.error(f"Error getting promo code with title {title}: {error}")
            raise error
