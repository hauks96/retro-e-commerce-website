# Generated by Django 3.0.5 on 2020-05-13 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20200512_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='product',
        ),
        migrations.AddField(
            model_name='tag',
            name='product',
            field=models.ManyToManyField(to='shop.Product'),
        ),
    ]