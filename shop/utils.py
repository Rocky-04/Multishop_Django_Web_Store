from django.db.models import Q
from django.views.generic import ListView

from .models import *


class ShopMixin(ListView):
    template_name = 'shop/shop.html'
    paginate_by = 9
    model = Product
    context_object_name = 'products'
    allow_empty = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_list_pk = []

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Всі товари'
        context['parent'] = None
        context['product_list_pk'] = self.product_list_pk

        context['color_filter'] = Color.objects.annotate(
            cnt=Count('color__product',
                      filter=Q(color__product__in=self.product_list_pk))). \
            filter(cnt__gt=0).order_by('-cnt')

        context['size_filter'] = Size.objects.annotate(
            cnt=Count('size__product__product', filter=Q(
                size__product__product__in=self.product_list_pk))). \
            filter(cnt__gt=0).order_by('-cnt')

        context['manufacturer_filter'] = Manufacturer.objects.annotate(
            cnt=Count('manufacturer',
                      filter=Q(manufacturer__in=self.product_list_pk))). \
            filter(cnt__gt=0).order_by('-cnt')

        return context
