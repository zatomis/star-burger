# Generated by Django 3.2.15 on 2024-03-28 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(unique=True, verbose_name='адрес')),
                ('lon', models.FloatField(blank=True, null=True, verbose_name='долгота')),
                ('lat', models.FloatField(blank=True, null=True, verbose_name='широта')),
                ('last_check', models.DateTimeField(verbose_name='дата проверки координат')),
            ],
        ),
    ]