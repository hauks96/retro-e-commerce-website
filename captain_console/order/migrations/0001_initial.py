# Generated by Django 3.0.5 on 2020-05-11 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default='', max_length=15)),
                ('items', models.CharField(default='', max_length=300)),
                ('date', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(default='email@email.com', max_length=254)),
                ('full_name', models.CharField(blank=True, default='', max_length=70)),
                ('address', models.CharField(blank=True, default='', max_length=32)),
                ('country', models.CharField(blank=True, default='', max_length=32)),
                ('city', models.CharField(blank=True, default='', max_length=32)),
                ('postal_code', models.CharField(blank=True, default='', max_length=12)),
                ('note', models.CharField(blank=True, default='', max_length=100)),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='order.OrderStatus')),
            ],
        ),
    ]
