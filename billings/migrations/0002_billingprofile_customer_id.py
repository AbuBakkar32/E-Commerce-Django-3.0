# Generated by Django 2.2.3 on 2019-08-23 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingprofile',
            name='customer_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
