# Generated by Django 4.1.3 on 2022-11-21 05:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('basket', '0002_alter_productinbasket_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productinbasket',
            options={'verbose_name': 'Products in the basket',
                     'verbose_name_plural': 'Products in the basket'},
        ),
        migrations.RenameField(
            model_name='productinbasket',
            old_name='session_key',
            new_name='user_authenticated',
        ),
    ]