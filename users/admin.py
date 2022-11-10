from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    ordering = ('email',)
    list_display = ["email", "city", 'phone_number', 'is_superuser']
    fieldsets = (
        (_("Personal info"), {"fields": ("email",
                                         "first_name",
                                         "last_name",
                                         'birthday',
                                         "city",
                                         'phone_number',
                                         'address',
                                         'postcode',
                                         'additional_information',)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined",)}),
        (None, {"fields": ("password",)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(EmailForNews)
class EmailForNewsAdmin(admin.ModelAdmin):
    model = EmailForNews
