# Generated by Django 3.2.15 on 2022-11-12 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator_panel', '0013_auto_20221111_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidence',
            name='number',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='evidence',
            name='status',
            field=models.CharField(choices=[('new', 'Новий'), ('null', 'Нульовий'), ('taken', 'Врахований'), ('taken and paid', 'Врахований і оплачений')], max_length=20, verbose_name='Статус'),
        ),
    ]
