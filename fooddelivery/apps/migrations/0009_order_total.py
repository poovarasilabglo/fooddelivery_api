# Generated by Django 4.1.3 on 2022-11-27 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0008_alter_order_address_alter_order_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]