from django import template
from django.db.models import QuerySet

from news.services import count_news_from_categories
from news.services import get_all_categories

register = template.Library()


@register.simple_tag()
def get_categories() -> QuerySet:
    """
    Gets all categories
    """
    return get_all_categories()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    """
    Shows categories with articles and counts the news in the category
    """
    categories, cnt_news = count_news_from_categories()
    return {'categories': categories,
            'cnt_news': cnt_news}
