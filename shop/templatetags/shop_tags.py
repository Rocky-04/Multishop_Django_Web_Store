from django import template
from django.core.paginator import Paginator
from django.db.models import Count

from shop.models import Banner
from shop.models import Category
from shop.models import Manufacturer
from shop.models import Product
from shop.models import Reviews
from shop.models import Tag

register = template.Library()


@register.inclusion_tag('shop/inc/list_categories.html')
def show_category(title='Товар', parent=None):
    if parent is not False:
        category = Category.objects.filter(parent__exact=parent)
    else:
        category = []

    return {'category': category,
            'title': title}


@register.inclusion_tag('shop/inc/banner.html')
def show_banner(pk_banner):
    tag = Tag.objects.get(title=Banner.objects.get(pk=pk_banner).tag)
    return {'tag': tag}


@register.inclusion_tag('shop/inc/carousel_banner.html')
def show_carousel_banner(pk_banner):
    tag = Tag.objects.get(title=Banner.objects.get(pk=pk_banner).tag)
    return {'tag': tag}


@register.inclusion_tag('shop/inc/carousel_brand.html')
def show_carousel_brand():
    brand = Manufacturer.objects.annotate(cnt=Count('picture')).filter(
        cnt__gt=0)
    return {'brand': brand}


@register.inclusion_tag('shop/inc/card_product.html', takes_context=True)
def show_card_product(context, item):
    return {'item': item,
            'favorite_list': context['favorite_list'],
            'products_basket_list': context['products_basket_list'],
            'request': context['request']
            }


@register.simple_tag()
def get_products(limit=0, categoty_id=None, tag_id=None):
    products = Product.objects.all().order_by('-available', '-count_sale')
    if categoty_id:
        products = products.filter(category=categoty_id)
    if tag_id:
        products = products.filter(tags=tag_id)
    if limit and limit < len(products):
        products = products.all()[0:int(limit)]
    return products


@register.simple_tag()
def get_all_category():
    return Category.objects.all()


@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=1, on_ends=1):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number,
                                           on_each_side=on_each_side,
                                           on_ends=on_ends)


@register.simple_tag()
def get_color_in_product(products):
    print(products)

    return Category.objects.all()


@register.simple_tag()
def get_user_review(user_id, product_id):
    rewiew = Reviews.objects.filter(user_id=user_id, product=product_id)
    if len(rewiew) >= 1:
        return rewiew[0]
    else:
        return None


@register.simple_tag()
def get_fa_star(rating=5):
    if not rating:
        rating = 5
    else:
        rating = float(rating)
    star = ''
    for i in range(5):
        if rating >= 1:
            star += '<i class="fas fa-star text-primary mr-1"></i>'
        elif rating > 0.3:
            star += '<i class="fas fa-star-half-alt text-primary mr-1"></i>'
        else:
            star += '<i class="far fa-star text-primary mr-1"></i>'
        rating -= 1
    return star
