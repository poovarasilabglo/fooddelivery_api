# Generated by Django 4.1.3 on 2022-11-27 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_order_address_order_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=10),
        ),
    ]
