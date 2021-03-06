# Generated by Django 3.1.1 on 2020-10-16 09:54
from datetime import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_details_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membership',
            options={},
        ),
        migrations.RemoveField(
            model_name='employee',
            name='purchase_date',
        ),
        migrations.AlterField(
            model_name='membership',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.now(), verbose_name='Created'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='membership',
            name='currency',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='membership',
            name='level',
            field=models.IntegerField(default=0, verbose_name='level'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='membership',
            name='name',
            field=models.CharField(default='Free', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='membership',
            name='price',
            field=models.IntegerField(default=0, verbose_name='price'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='membership',
            name='product',
            field=models.CharField(default='null', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='membership',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.now(), verbose_name='Updated'),
            preserve_default=False,
        ),
    ]
