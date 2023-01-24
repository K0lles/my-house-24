# Generated by Django 3.2.15 on 2023-01-18 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_management', '0002_auto_20230117_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='director_photo',
            field=models.ImageField(blank=True, null=True, upload_to='about-us/photo/director'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='additional_text',
            field=models.TextField(blank=True, null=True, verbose_name='Короткий текст'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='additional_title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='short_text',
            field=models.TextField(blank=True, null=True, verbose_name='Короткий текст'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Заголовок'),
        ),
    ]