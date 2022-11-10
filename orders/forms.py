from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from orders.models import Order
from orders.models import PaymentMethod
from orders.models import PromoCode


class CreateOrderForm(ModelForm):
    email = forms.EmailField(label='E-mail',
                             help_text='exemple@gmail.com',
                             required=True,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control'}))
    first_name = forms.CharField(label=_("Ім'я"),
                                 help_text='John',
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control'}))
    last_name = forms.CharField(label=_('Прізвище'),
                                help_text='Doe',
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control'}))
    city = forms.EmailField(label=_("Місто"),
                            help_text='Kyiv',
                            required=False,
                            widget=forms.EmailInput(
                                attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label=_("Телефон"),
                                   help_text='+38063000000',
                                   required=True,
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

    payment_method = ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=PaymentMethod.objects.all())
    promo_code = forms.CharField(label=_("Промо код"),
                                 required=False,
                                 widget=forms.TextInput(
                                     attrs={"class": 'form-control'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'city', 'phone_number',
                  'address', 'postcode', 'additional_information',
                  'payment_method')

    def clean_promo_code(self):
        promo_code = self.cleaned_data['promo_code']
        if not promo_code:
            return promo_code
        try:
            promo_code = PromoCode.objects.get(title=promo_code)
            if promo_code.is_active:
                return self.cleaned_data['promo_code']
            else:
                raise ValidationError(_('Промокод не активний'))
        except Exception as ex:
            print(ex)
            raise ValidationError(_('Промокод не активний'))
