# Generated by Django 4.2.16 on 2024-10-25 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_cartitem_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='price',
        ),
    ]
