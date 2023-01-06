from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManger(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    A model for representing a user in the system.
    """
    username = None
    email = models.EmailField(_('email address'), unique=True, )
    city = models.CharField(max_length=200, blank=True, default=None, null=True)
    phone_number = models.CharField(max_length=200, blank=True, default=None, null=True)
    address = models.CharField(max_length=200, blank=True, default=None, null=True)
    postcode = models.CharField(max_length=200, blank=True, default=None, null=True)
    additional_information = models.CharField(max_length=300, blank=True, default=None, null=True)
    birthday = models.DateField(auto_now=False, auto_now_add=False, blank=True, default=None,
                                null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManger()

    def __str__(self):
        """
        Returns a string representation of the user.
        If the user has a first and last name, return a combination of the two.
        If the user only has a first name or last name, return only that.
        If the user has neither, return their email address.

        :return: A string representation of the user.
        """
        name = str(self.first_name) + ' ' + str(self.last_name)
        if len(name) == 1:
            name = self.email
        return name

    def get_review_name(self):
        """
        Get the name of the review.

        This method returns the `first_name` field of the `Reviews` object if it is not empty.
        Otherwise, it returns the string "anonymous".

        :return: The name of the review.
        """
        if self.first_name:
            return self.first_name
        else:
            return 'anonymous'


class EmailForNews(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
