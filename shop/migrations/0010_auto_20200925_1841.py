# Generated by Django 3.0.8 on 2020-09-25 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20200925_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='review',
            field=models.CharField(blank=True, default='', max_length=2038),
        ),
    ]