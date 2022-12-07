from django.db.models import Count
from django.db.models import F
from django.db.models import QuerySet

from news.models import Category
from news.models import News


def count_news_from_categories() -> tuple:
    """
    Get categories with articles and counts the news in the category
    categories: QuerySet
    cnt_news: dict
    """
    categories = Category.objects.annotate(
        cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0).order_by('-cnt')
    cnt_news = News.objects.filter(is_published=True).aggregate(Count('pk'))
    return categories, cnt_news


def get_all_categories() -> QuerySet:
    """
    Gets all categories
    """
    return Category.objects.all()
