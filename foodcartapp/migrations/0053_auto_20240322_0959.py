# Generated by Django 3.2.15 on 2024-03-22 06:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0052_rename_comments_userorder_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userorder',
            name='order_date',
        ),
        migrations.AddField(
            model_name='userorder',
            name='call_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Дата звонка', verbose_name='Созвон'),
        ),
        migrations.AddField(
            model_name='userorder',
            name='delivered_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Дата доставки', verbose_name='Доставка'),
        ),
        migrations.AddField(
            model_name='userorder',
            name='registr_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Дата регистрации заказа', verbose_name='Заказ'),
        ),
    ]
