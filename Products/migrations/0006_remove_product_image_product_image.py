# Generated by Django 4.2.16 on 2024-10-25 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0005_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Image',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=1, upload_to='photos/'),
            preserve_default=False,
        ),
    ]