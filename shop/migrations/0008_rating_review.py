# Generated by Django 3.0.8 on 2020-09-17 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_ordersummary_review_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='review',
            field=models.CharField(default='', max_length=2038),
        ),
    ]