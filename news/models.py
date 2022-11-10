from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey('Category', related_name='news',
                                 on_delete=models.PROTECT, null=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True,
                            db_index=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('news_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _('Новини')
        verbose_name_plural = _('Новини')
        ordering = ['-created_at', 'title']


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True,
                            db_index=True)

    def get_absolute_url(self):
        return reverse_lazy('news_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']
