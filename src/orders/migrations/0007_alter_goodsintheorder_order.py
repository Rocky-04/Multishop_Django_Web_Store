# Generated by Django 4.1.1 on 2022-10-20 10:10

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0006_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsintheorder',
            name='order',
            field=models.ForeignKey(blank=True, default=None, null=True,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    related_name='goods_in_the_order',
                                    to='orders.order'),
        ),
    ]