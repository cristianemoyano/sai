# Generated by Django 2.0.9 on 2019-01-04 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_productcategory_parameter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='price',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='price',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='productstatus',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='productstatus',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='productstore',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='productstore',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='producttype',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='producttype',
            name='modified_date',
        ),
        migrations.AddField(
            model_name='currency',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='currency',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='price',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='price',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='productstatus',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='productstatus',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='productstore',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='productstore',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='producttype',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='producttype',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
