from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import GoodsInTheOrder
from .models import Order
from .models import PaymentMethod
from .models import PromoCode
from .models import Status


@admin.register(Status)
class StatusAdmin(TranslationAdmin):
    list_display = ('title',)


class ProductInOrderInline(admin.StackedInline):
    model = GoodsInTheOrder
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'city',
                    'phone_number', 'updated', 'total_price',
                    'payment_method']
    inlines = [ProductInOrderInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["total_price", 'delivery', 'user']
        else:
            return []


@admin.register(GoodsInTheOrder)
class GoodsInTheOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GoodsInTheOrder._meta.fields]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["total_price", "price_per_item"]
        else:
            return []


@admin.register(PaymentMethod)
class PaymentMethodAdmin(TranslationAdmin):
    model = PaymentMethod


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    model = PromoCode
