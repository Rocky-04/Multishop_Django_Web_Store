from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from mptt.admin import DraggableMPTTAdmin
from nested_admin import NestedModelAdmin
from nested_admin import NestedStackedInline

from .forms import ColorForm
from .forms import SizeForm
from .forms import SizeInlineFormSet
from .models import *


class AttributeColorImageAdmin(admin.StackedInline):
    model = AttributeColorImage
    min_num = 1
    max_num = 10
    extra = 0


class AttributeColorInline(admin.StackedInline):
    model = AttributeColor
    min_num = 1
    extra = 3


class AttributeSizeLevelTwo(NestedStackedInline, admin.StackedInline):
    model = AttributeSize
    min_num = 7
    max_num = 7
    extra = 0
    form = SizeForm
    formset = SizeInlineFormSet


class AttributeColorImageAdminLevelTwo(NestedStackedInline):
    model = AttributeColorImage
    max_num = 10
    min_num = 1
    extra = 0


class AttributeColorInlineLevelOne(NestedStackedInline):
    min_num = 1
    extra = 0
    exclude = ("available",)
    model = AttributeColor
    form = ColorForm

    inlines = [AttributeSizeLevelTwo, AttributeColorImageAdminLevelTwo]


@admin.register(Product)
class ProductAdminLevel(NestedModelAdmin, TranslationAdmin):
    model = Product

    prepopulated_fields = {'slug': ('title',)}
    list_display = (
        'id', 'title', 'price', 'price_now', 'discount', 'count_sale',
        'available', 'manufacturer', 'created_at',
        'category')
    list_display_links = ('id', 'title')
    exclude = ("available",)
    search_fields = ('title', 'id')
    list_editable = ('discount',)
    list_filter = ('category', 'available', 'manufacturer')
    readonly_fields = ('created_at',)
    save_as = True
    save_on_top = True
    inlines = [AttributeColorInlineLevelOne]


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    param = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(AttributeColor)
class AttributeColorAdmin(admin.ModelAdmin):
    """all"""
    list_display = [field.name for field in AttributeColor._meta.fields]
    inlines = [AttributeColorImageAdmin]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title', 'id')
    search_fields = ('title', 'id')
    list_filter = ('title',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'slug')
    list_display_links = ('title', 'id')
    search_fields = ('title', 'id')
    list_filter = ('title',)


@admin.register(Country)
class CountryAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'slug')
    list_display_links = ('title', 'id')
    search_fields = ('title', 'id')
    list_filter = ('title',)


@admin.register(Category)
class CustomMPTTModelAdmin(DraggableMPTTAdmin, TranslationAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'id')
    mptt_level_indent = 10


@admin.register(Delivery)
class DeliveryAdmin(TranslationAdmin):
    list_display = [field.name for field in Delivery._meta.fields]


@admin.register(Tag)
class TagAdmin(TranslationAdmin):
    list_display = [field.name for field in Tag._meta.fields]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Banner)
class BannerAdmin(TranslationAdmin):
    list_display = [field.name for field in Banner._meta.fields]


@admin.register(Color)
class ColorAdmin(TranslationAdmin):
    list_display = [field.name for field in Color._meta.fields]


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Size._meta.fields]


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Reviews._meta.fields]
