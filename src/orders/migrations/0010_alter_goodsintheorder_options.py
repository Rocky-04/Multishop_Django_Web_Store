# Generated by Django 4.1.3 on 2023-01-13 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_paymentmethod_title_en_paymentmethod_title_uk_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goodsintheorder',
            options={'verbose_name': 'Goods in the order', 'verbose_name_plural': 'Goods in the orders'},
        ),
    ]