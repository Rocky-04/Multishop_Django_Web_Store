import logging

from django.http import HttpResponseNotFound
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Category
from .models import News

logger = logging.getLogger(__name__)


class NewsView(ListView):
    """
    Renders a list of published news.
    """
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news'
    allow_empty = True
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Adds the title to the context data.

        :param object_list: The list of objects.
        :param kwargs: Additional keyword arguments.
        :return: The modified context data.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = _('News')
        return context

    def get_queryset(self):
        """
        Filters the queryset to only include published news.

        :return: The filtered queryset.
        """
        return News.objects.filter(is_published=True).select_related('category')


class NewsCategoryView(ListView):
    """
    Renders a list of published news for a given category.
    """
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news'
    slug_url_kwarg = 'slug'
    allow_empty = True
    paginate_by = 5

    def get_queryset(self):
        """
        Filters the queryset to only include published news in the specified category.

        :return: The filtered queryset.
        """
        return News.objects.filter(category__slug=self.kwargs['slug'],
                                   is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Adds the category name to the context data.

        :param object_list: The list of objects.
        :param kwargs: Additional keyword arguments.
        :return: The modified context data.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class NewsDetailView(DetailView):
    """
    Renders the details of a specific news item.
    """
    model = News
    template_name = "news/news_detail.html"
    context_object_name = 'item'

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except News.DoesNotExist as error:
            logger.error(f"Error getting news item: {error}")
            return HttpResponseNotFound("News item not found")
