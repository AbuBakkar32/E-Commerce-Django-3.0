# Generated by Django 2.2.3 on 2019-08-28 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0003_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='default',
            field=models.BooleanField(default=True),
        ),
    ]
