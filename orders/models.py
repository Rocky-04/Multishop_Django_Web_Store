from django.db import models
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from shop.models import AttributeColor
from shop.models import AttributeSize
from shop.models import Delivery
from shop.models import Product
from users.models import User


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
    total_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      default=0)
    status = models.ForeignKey('Status', default=1, on_delete=models.SET_NULL,
                               blank=True, null=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL,
                                 blank=True, null=True, default=None)
    payment_method = models.ForeignKey('PaymentMethod',
                                       on_delete=models.SET_NULL, blank=True,
                                       null=True, default=None)
    promo_code = models.ForeignKey('PromoCode', on_delete=models.SET_NULL,
                                   blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class GoodsInTheOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True,
                                null=True, default=None)
    color = models.ForeignKey(AttributeColor, on_delete=models.SET_NULL,
                              blank=True, null=True, default=None)
    size = models.ForeignKey(AttributeSize, on_delete=models.SET_NULL,
                             blank=True, null=True, default=None)
    order = models.ForeignKey(Order, related_name="goods_in_the_order",
                              on_delete=models.CASCADE, blank=True, null=True,
                              default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      default=0)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2,
                                         default=0)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'goods in the order'
        verbose_name_plural = 'goods in the orders'

    def save(self, *args, **kwargs):
        self.price_per_item = self.product.price_now
        self.total_price = self.nmb * self.price_per_item
        super(GoodsInTheOrder, self).save(*args, **kwargs)


class Status(models.Model):
    title = models.CharField(max_length=24, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


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


def product_in_order_post_save(sender, instance, created=None, **kwargs):
    order = instance.order
    all_products_in_order = GoodsInTheOrder.objects.filter(order=order)
    promo_code = 0
    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    if order_total_price:
        delivery = Delivery.get_delivery(order_total_price)
        instance.order.delivery = delivery
        delivery = delivery.price
        if instance.order.promo_code:
            promo_code = instance.order.promo_code.price

    else:
        instance.order.delivery = None
        delivery = 0

    total_price = order_total_price + delivery - promo_code
    instance.order.total_price = 0 if total_price < 0 else total_price
    instance.order.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=GoodsInTheOrder)
post_delete.connect(product_in_order_post_save, sender=GoodsInTheOrder)
