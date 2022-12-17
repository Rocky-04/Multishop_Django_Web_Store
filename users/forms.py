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
    first_name = forms.CharField(label=_("First name"),
                                 required=False,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control'}))
    last_name = forms.CharField(label=_('Last name'),
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'}))
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_('Repeat the password'),
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
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
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
    new_password1 = forms.CharField(label=_('Password'),
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label=_('Repeat the password'),
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control'}))


class UpdateUserDataForm(ModelForm):
    first_name = forms.CharField(label=_("First name"),
                                 help_text='John',
                                 required=False,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control'}))
    last_name = forms.CharField(label=_('Last name'),
                                help_text='Doe',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'}))
    city = forms.CharField(label=_("City"),
                           help_text='Kyiv',
                           required=False,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label=_("Phone"),
                                   required=False,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control'}))
    address = forms.CharField(label=_("Address"),
                              help_text='123 Street',
                              required=False,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control'}))
    postcode = forms.CharField(label=_("Postcode"),
                               help_text='16730',
                               required=False,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    additional_information = forms.CharField(label=_("Additional Information"),
                                             help_text='wish',
                                             required=False,
                                             widget=forms.TextInput(attrs={
                                                 'class': 'form-control'}))
    birthday = forms.DateField(label=_("Date of birth: 10/10/2000"),
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
        """
        Validate the email field.

        This method checks that the email entered in the `email` field is not already present in
        the `EmailForNews` table. If the email already exists, it raises a validation error.

        :return: The email value if it is valid.
        :raises forms.ValidationError: If the email is already present in the `EmailForNews` table.
        """
        email = self.cleaned_data['email']

        if EmailForNews.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(
                _('Such an email has already been added to the mailing list'))
        return email


class CommunicationForm(forms.ModelForm):
    is_active = forms.BooleanField(label=_("Receive letters in the mail?"),
                                   required=False,
                                   )

    class Meta:
        model = EmailForNews
        fields = ('is_active',)
