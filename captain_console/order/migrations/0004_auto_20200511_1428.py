# Generated by Django 3.0.5 on 2020-05-11 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='order',
            old_name='order_date',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_file',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_status',
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='email@email.com', max_length=254),
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='order.OrderStatus'),
        ),
    ]