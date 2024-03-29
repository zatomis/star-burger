# Generated by Django 3.2.15 on 2024-03-01 06:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_alter_userorder_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userorder',
            name='product',
        ),
        migrations.RemoveField(
            model_name='userorder',
            name='quantity',
        ),
        migrations.AddField(
            model_name='userorder',
            name='comments',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
        migrations.CreateModel(
            name='OrderState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(default=0, verbose_name='Кол-во заказа')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='foodcartapp.userorder', verbose_name='заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='foodcartapp.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'Состояние заказа',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
