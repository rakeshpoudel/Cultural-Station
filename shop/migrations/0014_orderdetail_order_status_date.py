# Generated by Django 3.0.8 on 2020-10-06 07:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20201004_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='order_status_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
