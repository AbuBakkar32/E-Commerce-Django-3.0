# Generated by Django 2.2.6 on 2019-10-26 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20191023_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_by',
            field=models.CharField(choices=[('cash_on_delivery', 'Cash On Delivery'), ('bkash', 'Bkash'), ('card', 'Card'), ('rocket', 'Rocket')], default='card', max_length=20),
        ),
    ]
