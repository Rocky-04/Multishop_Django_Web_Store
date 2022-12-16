import logging

from django import template
from django.db.models import QuerySet

from news.services import count_news_from_categories
from news.services import get_all_categories

register = template.Library()
logger = logging.getLogger(__name__)


@register.simple_tag()
@register.simple_tag()
def get_categories() -> QuerySet:
    """
    Retrieves all news categories from the database.

    :return: A queryset of all categories.
    """
    try:
        return get_all_categories()
    except Exception as error:
        logger.error(f"Error getting categories: {error}")
        return None


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    """
    Shows categories with articles and counts the news in the category
    """
    categories, cnt_news = count_news_from_categories()
    return {'categories': categories,
            'cnt_news': cnt_news}
