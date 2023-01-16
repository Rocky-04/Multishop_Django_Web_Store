# Generated by Django 4.1.1 on 2022-10-18 14:40

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('shop', '0008_delete_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=24)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('city', models.CharField(blank=True, max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=200)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('postcode', models.CharField(blank=True, max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('additional_information',
                 models.TextField(blank=True, max_length=300)),
                ('total_price',
                 models.DecimalField(decimal_places=2, default=0,
                                     max_digits=10)),
                ('delivery',
                 models.ForeignKey(blank=True, default=None, null=True,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   to='shop.delivery')),
                ('payment_method',
                 models.ForeignKey(blank=True, default=None, null=True,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   to='orders.paymentmethod')),
                ('status',
                 models.ForeignKey(default=1,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   to='orders.status')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='GoodsInTheOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('total_price',
                 models.DecimalField(decimal_places=2, default=0,
                                     max_digits=10)),
                ('nmb', models.IntegerField(default=1)),
                ('price_per_item',
                 models.DecimalField(decimal_places=2, default=0,
                                     max_digits=10)),
                ('order',
                 models.ForeignKey(blank=True, default=None, null=True,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   to='orders.order')),
                ('product',
                 models.ForeignKey(blank=True, default=None, null=True,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   to='shop.product')),
            ],
            options={
                'verbose_name': 'goods in the order',
                'verbose_name_plural': 'goods in the orders',
            },
        ),
    ]