# Generated by Django 5.1.1 on 2025-04-16 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0002_address_apartment_address_room_number_extras_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='log',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
