# Generated by Django 2.0.9 on 2018-12-30 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcategory',
            name='parameter',
        ),
    ]
