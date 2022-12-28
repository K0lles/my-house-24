# Generated by Django 3.2.15 on 2022-12-28 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrator_panel', '0037_application_created_by_director'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Майстер'),
        ),
    ]
