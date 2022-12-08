from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from .models import *
from .services import get_color_filter
from .services import get_manufacturer_filter
from .services import get_size_filter


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
        context['title'] = _("All products")
        context['parent'] = None
        context['product_list_pk'] = self.product_list_pk
        context['color_filter'] = get_color_filter(self.product_list_pk)
        context['size_filter'] = get_size_filter(self.product_list_pk)
        context['manufacturer_filter'] = get_manufacturer_filter(self.product_list_pk)
        return context
