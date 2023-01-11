from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import register

from .models import Banner
from .models import Category
from .models import Color
from .models import Country
from .models import Delivery
from .models import Product
from .models import Tag


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('title', 'title_two', 'description')


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Product)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'param',)


@register(Color)
class ColorTranslationOptions(TranslationOptions):
    fields = ('value',)


@register(Delivery)
class DeliveryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ('title',)
