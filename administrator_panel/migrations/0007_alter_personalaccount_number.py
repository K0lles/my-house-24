# Generated by Django 3.2.15 on 2022-10-31 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator_panel', '0006_alter_personalaccount_flat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalaccount',
            name='number',
            field=models.CharField(max_length=255, unique=True, verbose_name='Номер'),
        ),
    ]