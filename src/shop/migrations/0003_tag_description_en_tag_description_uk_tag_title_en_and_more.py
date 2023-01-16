# Generated by Django 4.1.1 on 2022-10-17 16:57

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0002_category_title_en_category_title_uk'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='description_en',
            field=models.TextField(blank=True, default=None, null=True,
                                   verbose_name='Опис'),
        ),
        migrations.AddField(
            model_name='tag',
            name='description_uk',
            field=models.TextField(blank=True, default=None, null=True,
                                   verbose_name='Опис'),
        ),
        migrations.AddField(
            model_name='tag',
            name='title_en',
            field=models.CharField(max_length=50, null=True, unique=True,
                                   verbose_name='Назва'),
        ),
        migrations.AddField(
            model_name='tag',
            name='title_two_en',
            field=models.CharField(blank=True, max_length=50, null=True,
                                   verbose_name='Назва 2'),
        ),
        migrations.AddField(
            model_name='tag',
            name='title_two_uk',
            field=models.CharField(blank=True, max_length=50, null=True,
                                   verbose_name='Назва 2'),
        ),
        migrations.AddField(
            model_name='tag',
            name='title_uk',
            field=models.CharField(max_length=50, null=True, unique=True,
                                   verbose_name='Назва'),
        ),
    ]