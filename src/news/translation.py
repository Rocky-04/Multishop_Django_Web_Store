from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import register

from news.models import Category
from news.models import News


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')
