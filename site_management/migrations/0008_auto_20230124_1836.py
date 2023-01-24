# Generated by Django 3.2.15 on 2023-01-24 16:36

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('site_management', '0007_tariffobjectfront_tariffpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Адреса'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='commercial_url',
            field=models.URLField(blank=True, null=True, verbose_name='Посилання на комерційний сайт'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Локація'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='map_code',
            field=models.TextField(blank=True, null=True, verbose_name='Код карти'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name_surname_father',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='ПІБ'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Короткий текст'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Заголовок'),
        ),
    ]