# Generated by Django 4.1.3 on 2022-11-28 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0011_restaurant_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='user',
        ),
    ]
