# Generated by Django 3.2.15 on 2024-03-18 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_orderstate_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderstate',
            old_name='cost',
            new_name='price',
        ),
    ]
