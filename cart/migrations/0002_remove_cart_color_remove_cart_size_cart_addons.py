# Generated by Django 5.1.1 on 2025-03-12 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('posts', '0007_alter_brand_radius'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='color',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='size',
        ),
        migrations.AddField(
            model_name='cart',
            name='addons',
            field=models.ManyToManyField(blank=True, related_name='cart_addons', to='posts.product'),
        ),
    ]
