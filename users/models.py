from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = None
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    city = models.CharField(max_length=200, blank=True, default=None,
                            null=True)
    phone_number = models.CharField(max_length=200, blank=True, default=None,
                                    null=True)
    address = models.CharField(max_length=200, blank=True, default=None,
                               null=True)
    postcode = models.CharField(max_length=200, blank=True, default=None,
                                null=True)
    additional_information = models.CharField(max_length=300, blank=True,
                                              default=None, null=True)
    birthday = models.DateField(auto_now=False, auto_now_add=False, blank=True,
                                default=None, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        name = str(self.first_name) + ' ' + str(self.last_name)
        if len(name) == 1:
            name = self.email
        return name

    def get_review_name(self):
        if self.first_name:
            return self.first_name
        else:
            return 'anonymous'


class EmailForNews(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
