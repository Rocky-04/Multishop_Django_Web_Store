from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import \
    PasswordResetConfirmView as PasswordResetConfirmView_
from django.contrib.auth.views import PasswordResetView as PasswordResetView_
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from basket.models import ProductInBasket
from favorite.models import Favorite
from orders.models import Order
from shop.models import Reviews
from .forms import CommunicationForm
from .forms import PasswordResetForm
from .forms import SetPasswordForm
from .forms import SubscriberEmailForm
from .forms import UpdateUserDataForm
from .forms import UserLoginForm
from .forms import UserRegisterForm
from .models import EmailForNews
from .models import User


class LoginUserView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Авторизація')
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.data['username']
        ProductInBasket.objects.filter(session_key=session_key).update(
            session_key=user)
        Favorite.objects.filter(session_key=session_key).update(
            session_key=user)
        return super().form_valid(form)


class RegisterUserView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Реєстрація')
        return context

    def form_valid(self, form):
        user = form.save()
        session_key = self.request.session.session_key
        ProductInBasket.objects.filter(session_key=session_key).update(
            session_key=user.email)
        Favorite.objects.filter(session_key=session_key).update(
            session_key=user.email)
        EmailForNews.objects.create(email=user.email)
        login(self.request, user)
        return redirect('home')


class AccountUserView(TemplateView):
    template_name = 'users/orders.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(Q(user=self.request.user) | Q(
            email=self.request.user.email)).order_by('-id')

        context['orders'] = orders
        context['title'] = _('Мої замовлення')
        return context


class AccountDataUserView(UpdateView):
    model = User
    template_name = 'users/account_data.html'
    success_url = reverse_lazy('account_data')
    form_class = UpdateUserDataForm

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            obj = User.objects.get(id=self.request.user.pk)
            return obj
        raise Http404()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Мої дані')
        return context


def logout_user_view(requests):
    logout(requests)
    return redirect('home')


class PasswordResetView(PasswordResetView_):
    form_class = PasswordResetForm
    from_email = 'rocky113@ukr.net'


class PasswordResetConfirmView(PasswordResetConfirmView_):
    form_class = SetPasswordForm


def subscriber_email(request):
    current = request.POST.get('current')
    if request.method == 'POST':
        form = SubscriberEmailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Email додано'))
            return HttpResponseRedirect(current)
    else:
        form = SubscriberEmailForm()
    return render(request, 'users/subscriber_email.html', {'form': form})


class CommunicationView(UpdateView):
    template_name = 'users/communication.html'
    form_class = CommunicationForm
    model = EmailForNews
    success_url = reverse_lazy('communication')

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            try:
                obj = EmailForNews.objects.get(email=self.request.user.email)
            except Exception as ex:
                print(ex)
                obj = EmailForNews.objects.create(
                    email=self.request.user.email)

            return obj
        raise Http404()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Комунікації')
        context['email'] = self.request.user.email
        return context


class MyProductReviewView(ListView):
    template_name = 'users/my_product_review.html'
    context_object_name = 'rewiews'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Мої відгуки')
        return context

    def get_queryset(self):
        return Reviews.objects.filter(user=self.request.user)
