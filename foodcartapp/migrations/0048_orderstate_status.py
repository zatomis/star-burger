# Generated by Django 3.2.15 on 2024-03-21 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_OrderState_add_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstate',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Необработанный'), (1, 'Принят в работу'), (2, 'Заказ на сборке'), (3, 'Передан курьеру'), (4, 'Заказ выполнен')], db_index=True, default=0, verbose_name='Статус заказа'),
        ),
    ]
