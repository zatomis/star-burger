# Generated by Django 3.2.15 on 2024-04-07 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0058_auto_20240407_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorder',
            name='available_restaurants',
            field=models.ManyToManyField(blank=True, to='foodcartapp.Restaurant', verbose_name='доступные рестораны'),
        ),
    ]
