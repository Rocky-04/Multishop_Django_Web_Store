import logging
from typing import Dict
from typing import Union

from django import template
from django.db.models import QuerySet

from news.services import count_news_from_categories
from news.services import get_all_categories

register = template.Library()
logger = logging.getLogger(__name__)


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
def show_categories() -> Dict[str, Union[QuerySet, int]]:
    """
    Renders a list of categories with articles and counts the number of news in each category.

    :return: A dictionary containing the categories queryset and a dictionary of category counts.
    """
    try:
        categories, cnt_news = count_news_from_categories()
        return {'categories': categories,
                'cnt_news': cnt_news}
    except Exception as error:
        logger.error(f"Error showing categories: {error}")
        return {'categories': None, 'cnt_news': None}
