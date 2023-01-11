from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from .models import *
from .services import filter_colors_by_products
from .services import filter_manufacturers_by_products
from .services import filter_size_by_products


class ShopMixin(ListView):
    """
    Generic mixin is for a product listing page

    Passes the following data to the template:
    :title: Page title
    :parent: The ID of the parent category to filter by.
    :product_list_pk: List of product PKs
    :color_filter: A queryset of colors that are associated with the given products
    :size_filter: A queryset of size that are associated with the given products
    :manufacturer_filter: A queryset of manufacturer that are associated with the given products
    """
    template_name = 'shop/shop.html'
    paginate_by = 9
    model = Product
    context_object_name = 'product_list'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("All products")
        context['parent'] = None
        context['product_list_pk'] = self.product_list_pk
        context['color_filter'] = filter_colors_by_products(self.product_list_pk)
        context['size_filter'] = filter_size_by_products(self.product_list_pk)
        context['manufacturer_filter'] = filter_manufacturers_by_products(self.product_list_pk)
        return context
