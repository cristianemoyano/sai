# Generated by Django 2.0.9 on 2019-01-18 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_auto_20190104_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='identifier_number',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]