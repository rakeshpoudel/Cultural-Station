# Generated by Django 3.0.5 on 2020-06-15 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_cancellation_product_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_details',
        ),
    ]
