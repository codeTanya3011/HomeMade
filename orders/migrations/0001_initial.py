# Generated by Django 5.1.7 on 2025-03-23 18:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Order creation date')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Phone number')),
                ('requires_delivery', models.BooleanField(default=False, verbose_name='Delivery required')),
                ('delivery_address', models.TextField(blank=True, null=True, verbose_name='Delivery address')),
                ('payment_on_get', models.BooleanField(default=False, verbose_name='Payment upon receipt')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Paid')),
                ('status', models.CharField(default='In processing', max_length=50, verbose_name='Order status')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'order',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Price')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Quantity')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date of sale')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Order')),
                ('product', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='goods.products', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Sold item',
                'verbose_name_plural': 'Sold items',
                'db_table': 'order_item',
                'ordering': ('id',),
            },
        ),
    ]
