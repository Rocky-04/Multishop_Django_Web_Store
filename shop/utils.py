from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from .models import *
from .services import filter_colors_by_products
from .services import filter_manufacturers_by_products
from .services import filter_size_by_products


class ShopMixin(ListView):
    template_name = 'shop/shop.html'
    paginate_by = 9
    model = Product
    context_object_name = 'products'
    allow_empty = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_list_pk: list = []

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("All products")
        context['parent'] = None
        context['product_list_pk'] = self.product_list_pk
        context['color_filter'] = filter_colors_by_products(self.product_list_pk)
        context['size_filter'] = filter_size_by_products(self.product_list_pk)
        context['manufacturer_filter'] = filter_manufacturers_by_products(self.product_list_pk)
        return context
