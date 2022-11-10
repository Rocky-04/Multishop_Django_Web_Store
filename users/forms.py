from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm as ResetForm
from django.contrib.auth.forms import SetPasswordForm as SetPasswordForm_
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import EmailForNews
from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='E-mail',
                             required=True,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Ім'я",
                                 required=False,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Прізвище',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторіть пароль',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'captcha'
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('email', 'password',)


class PasswordResetForm(ResetForm):
    email = forms.CharField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    captcha = CaptchaField()


class SetPasswordForm(SetPasswordForm_):
    new_password1 = forms.CharField(label='Пароль',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Повторіть пароль',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control'}))


class UpdateUserDataForm(ModelForm):
    first_name = forms.CharField(label=_("Ім'я"),
                                 help_text='John',
                                 required=False,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control'}))
    last_name = forms.CharField(label=_('Прізвище'),
                                help_text='Doe',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'}))
    city = forms.CharField(label=_("Місто"),
                           help_text='Kyiv',
                           required=False,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label=_("Телефон"),
                                   required=False,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control'}))
    address = forms.CharField(label=_("Адреса"),
                              help_text='123 Street',
                              required=False,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control'}))
    postcode = forms.CharField(label=_("Індекс"),
                               help_text='16730',
                               required=False,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    additional_information = forms.CharField(label=_("Додаткова інформація"),
                                             help_text='wish',
                                             required=False,
                                             widget=forms.TextInput(attrs={
                                                 'class': 'form-control'}))
    birthday = forms.DateField(label=_('Дата народження: 10/10/2000'),
                               required=False,
                               widget=forms.DateInput(
                                   format='%d.%m.%Y',
                                   attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'city', 'phone_number',
                  'address', 'postcode', 'additional_information', 'birthday')


class SubscriberEmailForm(forms.ModelForm):
    email = forms.CharField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = EmailForNews
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']

        if EmailForNews.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(
                _('Такий email вже доданий до розсилки'))
        return email


class CommunicationForm(forms.ModelForm):
    is_active = forms.BooleanField(label=_("Отримувати листи на пошту?"),
                                   required=False,
                                   )

    class Meta:
        model = EmailForNews
        fields = ('is_active',)
