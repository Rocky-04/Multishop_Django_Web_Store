from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Category
from .models import News


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'created_at', 'updated_at', 'is_published', 'category')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'id')
    list_filter = ('is_published', 'category')
    list_editable = ('is_published',)
    fields = ('title', 'photo', 'content', 'is_published', 'category', 'slug')
    save_on_top = True


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
