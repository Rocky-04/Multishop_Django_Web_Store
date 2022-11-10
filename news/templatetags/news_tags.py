from django import template
from django.db.models import Count
from django.db.models import F

from news.models import Category
from news.models import News

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    categories = Category.objects.annotate(
        cnt=Count('news', filter=F('news__is_published'))).filter(
        cnt__gt=0).order_by('-cnt')
    cnt_news = News.objects.filter(is_published=True).aggregate(Count('pk'))
    return {'categories': categories,
            'cnt_news': cnt_news}
