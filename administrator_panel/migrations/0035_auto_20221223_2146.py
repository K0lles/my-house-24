# Generated by Django 3.2.15 on 2022-12-23 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator_panel', '0034_auto_20221223_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Опис'),
        ),
    ]
