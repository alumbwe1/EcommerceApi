# Generated by Django 5.1.1 on 2025-05-16 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_alter_brand_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='radius',
        ),
        migrations.AlterField(
            model_name='brand',
            name='rating',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
