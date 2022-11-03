# Generated by Django 3.2.15 on 2022-11-03 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator_panel', '0009_alter_personalaccount_flat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalaccount',
            name='status',
            field=models.CharField(choices=[('active', 'Активний'), ('inactive', 'Неактивний')], default='inactive', max_length=15, verbose_name='Статус'),
        ),
    ]
