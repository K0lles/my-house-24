# Generated by Django 3.2.15 on 2022-11-08 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0005_auto_20221026_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='owner_id',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Нотатки'),
        ),
    ]