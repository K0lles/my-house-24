# Generated by Django 3.2.15 on 2022-12-28 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrator_panel', '0038_alter_application_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='flat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator_panel.flat'),
        ),
        migrations.AddField(
            model_name='message',
            name='floor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator_panel.floor'),
        ),
        migrations.AddField(
            model_name='message',
            name='house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator_panel.house'),
        ),
        migrations.AddField(
            model_name='message',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator_panel.section'),
        ),
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ManyToManyField(blank=True, related_name='receivers', to=settings.AUTH_USER_MODEL),
        ),
    ]