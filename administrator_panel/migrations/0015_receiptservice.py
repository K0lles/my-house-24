# Generated by Django 3.2.15 on 2022-11-14 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0008_user_created_at'),
        ('administrator_panel', '0014_auto_20221112_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiptService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('price', models.FloatField()),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipt', to='administrator_panel.receipt')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='service', to='configuration.service')),
            ],
        ),
    ]
