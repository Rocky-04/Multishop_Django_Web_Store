from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Category
from .models import News


class NewsView(ListView):
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Новини')
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related(
            'category')


class NewsCategoryView(ListView):
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news'
    slug_url_kwarg = 'slug'
    allow_empty = False
    paginate_by = 5

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['slug'],
                                   is_published=True).select_related(
            'category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_detail.html"
    context_object_name = 'item'
