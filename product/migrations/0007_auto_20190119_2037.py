# Generated by Django 2.0.9 on 2019-01-19 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20190119_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
