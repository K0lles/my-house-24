# Generated by Django 3.2.15 on 2022-11-24 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator_panel', '0021_auto_20221124_2320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notoriety',
            name='owner',
        ),
        migrations.AddField(
            model_name='notoriety',
            name='number',
            field=models.CharField(default='null', max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notoriety',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Коментар'),
        ),
    ]
