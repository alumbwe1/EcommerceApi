# Generated by Django 5.1.1 on 2025-05-04 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0003_alter_address_lat_alter_address_log'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='room_number',
        ),
        migrations.AlterField(
            model_name='address',
            name='addressType',
            field=models.CharField(choices=[('home', 'Home'), ('office', 'Office'), ('school', 'School')], default='school', max_length=10),
        ),
    ]
