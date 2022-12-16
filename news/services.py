import logging
from typing import Dict
from typing import Tuple

from django.db.models import Count
from django.db.models import F
from django.db.models import QuerySet

from news.models import Category
from news.models import News

logger = logging.getLogger(__name__)


def count_news_from_categories() -> Tuple[QuerySet, Dict[str, int]]:
    """
    Retrieves categories with published articles and counts the number of news in each category.

    :return: A tuple containing a queryset of categories with published articles and a
        dictionary of category counts.
    """
    try:
        categories = Category.objects.annotate(
            cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0).order_by('-cnt')
        cnt_news = News.objects.filter(is_published=True).aggregate(Count('pk'))
        return categories, cnt_news
    except Exception as error:
        logger.error(f"Error getting categories and counts: {error}")
        return None, None


def get_all_categories() -> QuerySet:
    """
    Retrieves all categories from the database.

    :return: A queryset of all categories.
    """
    try:
        return Category.objects.all()
    except Exception as error:
        logger.error(f"Error getting categories: {error}")
        return None
