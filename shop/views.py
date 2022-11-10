from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView
from django.views.generic import TemplateView

from online_store.settings import EMAIL_HOST_USER
from .forms import ReviewsForm
from .utils import *


class FilterView(ShopMixin):
    def get_queryset(self):
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        self.product_list_pk = [int(i) for i in
                                self.request.GET.get('product_list_pk')[
                                1:-1].split(', ')]

        if self.request.GET.getlist("color"):
            filter_color = AttributeColor.objects.filter(
                Q(color__in=self.request.GET.getlist("color"))).values_list(
                'product', flat=True)
        else:
            filter_color = AttributeColor.objects.all().values_list('product',
                                                                    flat=True)

        if self.request.GET.getlist("size"):
            filter_size = AttributeSize.objects.filter(
                Q(size__in=self.request.GET.getlist("size"))).values_list(
                'product__product', flat=True)
        else:
            filter_size = AttributeSize.objects.all().values_list(
                'product__product', flat=True)

        if self.request.GET.getlist("manufacturer"):
            filter_manufacturer = Manufacturer.objects.filter(
                Q(id__in=self.request.GET.getlist(
                    "manufacturer"))).values_list('manufacturer', flat=True)
        else:
            filter_manufacturer = Manufacturer.objects.all().values_list(
                'manufacturer', flat=True)

        queryset = Product.objects.filter(Q(pk__in=self.product_list_pk) & Q
        (pk__in=filter_color) & Q
                                          (pk__in=filter_size) & Q
                                          (pk__in=filter_manufacturer) & Q
                                          (price_now__gte=min_price,
                                           price_now__lte=max_price))

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Фільтр'
        return context


class SkipFilterView(ShopMixin):
    def get_queryset(self):
        self.product_list_pk = [int(i) for i in
                                self.request.GET.get('product_list_pk')[
                                1:-1].split(', ')]
        queryset = Product.objects.filter(pk__in=self.product_list_pk)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Товари'
        return context


class ShopView(ShopMixin):
    def get_queryset(self):
        product = Product.objects.all()
        self.product_list_pk = list(product.values_list('pk', flat=True))
        return product


class CategoryView(ShopMixin):
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        list_categories_pk = Category.objects.get(
            slug=self.kwargs['slug']).get_list_nested_categories()
        product = Product.objects.filter(category_id__in=list_categories_pk)
        self.product_list_pk = list(product.values_list('pk', flat=True))
        return product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        context['slug'] = Category.objects.get(slug=self.kwargs['slug']).pk
        context['parent'] = Category.objects.get(slug=self.kwargs['slug']).id
        return context


class TagView(ShopMixin):
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        product = Product.objects.filter(
            tags=Tag.objects.get(slug=self.kwargs['slug']))
        self.product_list_pk = list(product.values_list('pk', flat=True))
        return product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        context['slug'] = Tag.objects.get(slug=self.kwargs['slug']).pk
        context['parent'] = False
        return context


class BrandView(ShopMixin):
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        product = Product.objects.filter(
            manufacturer=Manufacturer.objects.get(slug=self.kwargs['slug']))
        self.product_list_pk = list(product.values_list('pk', flat=True))
        return product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Manufacturer.objects.get(slug=self.kwargs['slug'])
        context['slug'] = Manufacturer.objects.get(slug=self.kwargs['slug']).pk
        context['parent'] = False
        return context


class HomeView(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'category'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Головна'
        return context

    def get_queryset(self):
        return Category.objects.all()


class ContactView(TemplateView):
    template_name = 'shop/info/contact.html'


class SendUserMailView(TemplateView):
    template_name = 'shop/info/contact.html'

    def post(self, request):
        data = request.POST
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        if name and email and subject and message:
            text_subject = f"contact form: {subject} {name}"
            text_message = f"You have received a new message from your website contact form.\n\n" \
                           f"Here are the details:\n\nName: {name}\n\n\nEmail: {email}\n\n" \
                           f"Subject: {subject}\n\nMessage: {message}"
            mail = send_mail(text_subject, text_message, EMAIL_HOST_USER,
                             [email], fail_silently=False)
            if mail:
                messages.success(request, _('Лист відправлено'))
            else:
                messages.error(request,
                               _('Помилка при відправці листа. Спробуйте пізніше'))
        else:
            messages.error(request,
                           _('Помилка при відправці листа. Спробуйте пізніше'))

        return render(request, self.template_name)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'context'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug=self.kwargs['slug'])
        active_color = self.request.GET.get('color')
        active_size = self.request.GET.get('size')

        try:
            if active_color is not None:
                context['active_color'] = product.attribute_color.get(
                    color_id=active_color)
            elif product.available:
                context['active_color'] = product.get_active_color()[0]
            else:
                context['active_color'] = \
                    AttributeColor.objects.filter(product=product)[0]
            if active_size is not None:
                context['active_size'] = context[
                    'active_color'].attribute_size.get(size_id=active_size)
            elif context['active_color'].available:
                context['active_size'] = \
                    context['active_color'].get_active_size()[0]
            else:
                context['active_size'] = \
                    context['active_color'].get_all_size()[0]
        except Exception as e:
            print(e)

        context['title'] = product
        context['product'] = product
        context['slug'] = product.category.pk
        context['colors'] = product.get_all_color()
        context['form'] = ReviewsForm

        return context


class AboutView(TemplateView):
    template_name = 'shop/info/about-us.html'


class HelpView(TemplateView):
    template_name = 'shop/info/help.html'


class TermsView(TemplateView):
    template_name = 'shop/info/terms.html'


class SearchView(ListView):
    template_name = 'shop/search.html'
    paginate_by = 9
    model = Product
    context_object_name = 'products'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пошук'
        context['text'] = f"text={self.request.GET.get('text')}&"
        context['empty'] = self.request.GET.get('text')
        return context

    def get_queryset(self):
        return Product.objects.filter(
            title__icontains=self.request.GET.get('text'))



class AddReviewView(View):
    def post(self, request):
        form = ReviewsForm(request.POST)

        if form.is_valid() and self.request.user.is_authenticated:
            text = form.data['text']
            rating = form.data['rating']
            user = self.request.user
            product_id = request.POST.get('product_id')
            current = request.POST.get('current')

            rewiew = Reviews.objects.filter(user=user, product=product_id)

            if len(rewiew) >= 1:
                rewiew.update(text=text,
                              rating=rating)
            else:
                Reviews.objects.create(user=user,
                                       product_id=product_id,
                                       text=text,
                                       rating=rating)
            return HttpResponseRedirect(current)
        else:
            return JsonResponse({'success': False, 'error': 'Not found user'},
                                status=400)


class PageNotFoundView(TemplateView):
    template_name = 'shop/page_not_found.html'
