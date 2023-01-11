from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import register

from .models import PaymentMethod
from .models import Status


@register(Status)
class StatusTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(PaymentMethod)
class PaymentMethodTranslationOptions(TranslationOptions):
    fields = ('title',)
