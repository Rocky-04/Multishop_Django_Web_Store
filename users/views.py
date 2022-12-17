import logging

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetConfirmView as PasswordResetConfirmView_
from django.contrib.auth.views import PasswordResetView as PasswordResetView_
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from .forms import CommunicationForm
from .forms import PasswordResetForm
from .forms import SetPasswordForm
from .forms import SubscriberEmailForm
from .forms import UpdateUserDataForm
from .forms import UserLoginForm
from .forms import UserRegisterForm
from .models import EmailForNews
from .models import User
from .services import add_email_to_the_mailing_list
from .services import get_email_from_email_the_news
from .services import get_user
from .services import get_user_orders
from .services import get_user_reviews
from .services import update_user_in_basket
from .services import update_user_in_favorite
from .ultis import AuthorizedUserMixin

logger = logging.getLogger(__name__)


class LoginUserView(LoginView):
    """
    A view for logging in users.

    This view subclasses Django's built-in `LoginView`, adding additional functionality for
    updating the user's session key in the `ProductInBasket` and `Favorite` models when the user
    successfully logs in. It also provides a custom form class and template, and adds a context
    variable for the page title.
    """
    form_class = UserLoginForm
    template_name = 'users/login.html'
    next_page = 'account'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Add the page title to the context data.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = _('Authorization')
        return context

    def form_valid(self, form):
        """
        Update the user's session key in the `ProductInBasket` and `Favorite` models.

        This method overrides the parent class's `form_valid` method to update the user's session
        key in the `ProductInBasket` and `Favorite` models when the user successfully logs in.

        :param form: The form object.
        :return: The parent class's `form_valid` method.
        """
        session_key = self.request.session.session_key
        user = form.data['username']
        update_user_in_basket(old_user=session_key, new_user=user)
        update_user_in_favorite(old_user=session_key, new_user=user)

        return super().form_valid(form)


class RegisterUserView(CreateView):
    """
    A view for registering new users.

    This view subclasses Django's built-in `CreateView`, providing a custom form class and template
    for creating new user accounts. It also adds additional functionality for updating the user's
    session key in the `ProductInBasket` and `Favorite` models when the user successfully registers,
    and for adding the user's email to the news mailing list.
    """
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Add the page title to the context data.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = _('Register')
        return context

    def form_valid(self, form):
        """
        Update the user's session key in the `ProductInBasket` and `Favorite` models, and add the
        user's email to the news mailing list.

        This method overrides the parent class's `form_valid` method to update the user's session
        key in the `ProductInBasket` and `Favorite` models, and to add the user's email to the
        news mailing list when the user successfully registers. It also logs the user in and
        redirects them to the home page.

        :param form: The form object.
        :return: A redirect to the home page.
        """
        user = form.save()
        session_key = self.request.session.session_key
        update_user_in_basket(old_user=session_key, new_user=user)
        update_user_in_favorite(old_user=session_key, new_user=user)
        add_email_to_the_mailing_list(email=user.email)
        login(self.request, user)
        return redirect('home')


class PasswordResetView(PasswordResetView_):
    """
    A view for resetting a user's password.
    """
    form_class = PasswordResetForm
    from_email = 'rocky113@ukr.net'


class PasswordResetConfirmView(PasswordResetConfirmView_):
    """
    A view for confirming a password reset.

    This view allows a user to confirm their password reset by providing a new password. The new
    password must meet the requirements specified in the `SetPasswordForm` form class.
    """
    form_class = SetPasswordForm


class AccountUserView(AuthorizedUserMixin, TemplateView):
    """
    A view for displaying a user's orders.
    """
    template_name = 'users/orders.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = get_user_orders(self.request)
        context['title'] = _('My orders')
        return context


class AccountDataUserView(AuthorizedUserMixin, UpdateView):
    """
    A view for updating a user's account information.
    """
    model = User
    template_name = 'users/account_data.html'
    success_url = reverse_lazy('account_data')
    form_class = UpdateUserDataForm

    def get_object(self, queryset=None):
        """
        Get the user object for the current user.

        This method retrieves the user object for the current user and returns it. If the user is
        not authenticated, a 404 error is logged and raised.

        :param queryset: A queryset of objects. This parameter is not used.
        :return: The user object for the current user.
        :raises Http404: If the user is not authenticated.
        """
        try:
            if self.request.user.is_authenticated:
                return get_user(self.request.user.pk)
            else:
                logger.warning("User isn't authenticated")
                raise Http404()
        except User.DoesNotExist as error:
            logger.error(f"User object does not exist: {error}")
            raise Http404()
        except Exception as error:
            logger.error(f"Error getting user object: {error}")
            raise error

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('My data')
        return context


class CommunicationView(AuthorizedUserMixin, UpdateView):
    """
    A view for managing communication preferences.
    """
    template_name = 'users/communication.html'
    form_class = CommunicationForm
    model = EmailForNews
    success_url = reverse_lazy('communication')

    def get_object(self, queryset=None):
        """
        Gets the email address object for the authenticated user.

        :param queryset: A queryset to use for retrieving the email address object.
        :return: The email address object for the authenticated user.
        :raises Http404: If the user is not authenticated.
        """
        if self.request.user.is_authenticated:
            try:
                obj = get_email_from_email_the_news(self.request.user.email)
            except Exception as error:
                logger.warning(error)
                obj = add_email_to_the_mailing_list(self.request.user.email)
            return obj
        raise Http404()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Communications')
        context['email'] = self.request.user.email
        return context


class MyProductReviewView(AuthorizedUserMixin, ListView):
    """
    A view for displaying a user's reviews.
    """
    template_name = 'users/my_product_review.html'
    context_object_name = 'reviews'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('My reviews')
        return context

    def get_queryset(self):
        return get_user_reviews(request=self.request)


def subscriber_email(request) -> HttpResponse:
    """
    Adds an email to the newsletter list.
    If the request method is 'POST', then a form is created with the request data
    and validated. If the form is valid, the email is added to the list and a
    success message is displayed. If the request method is not 'POST', then a form
    is created without data.

    :param request: The HTTP request.
    :return: An HTTP response.
    """
    current = request.POST.get('current')
    if request.method == 'POST':
        form = SubscriberEmailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Email added'))
            return HttpResponseRedirect(current)
    else:
        form = SubscriberEmailForm()
    return render(request, 'users/subscriber_email.html', {'form': form})


def logout_user_view(requests):
    """
    A view for logging out a user.

    This view logs out the current user and redirects them to the homepage.

    :param requests: The request object for the current user.
    :return: A redirect to the homepage.
    """
    logout(requests)
    return redirect('home')
