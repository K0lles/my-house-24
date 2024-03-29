# Generated by Django 3.2.15 on 2022-11-15 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator_panel', '0017_receipt_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptservice',
            name='total_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='is_completed',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='receiptservice',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='receiptservice',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
