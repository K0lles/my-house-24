# Generated by Django 3.2.15 on 2022-12-01 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator_panel', '0025_alter_personalaccount_rest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalaccount',
            name='rest',
        ),
    ]
