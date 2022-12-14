# Generated by Django 4.1.1 on 2022-11-28 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0009_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_status',
            field=models.IntegerField(choices=[(1, 'Success'), (2, 'On the way'), (3, 'Pending'), (4, 'Cancel order')], default=3),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.menucategory'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.restaurant'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.IntegerField(choices=[(1, 'Success'), (2, 'On the way'), (3, 'Pending'), (4, 'Cancel order')], default=1),
        ),
    ]
