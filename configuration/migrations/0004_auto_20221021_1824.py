# Generated by Django 3.2.15 on 2022-10-21 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0003_auto_20221017_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='tariff',
            name='description',
            field=models.TextField(default='Some description', verbose_name='Опис тарифу'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tariffservice',
            name='currency',
            field=models.CharField(default='грн', max_length=55, verbose_name='Валюта'),
        ),
    ]
