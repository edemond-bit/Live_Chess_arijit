# Generated by Django 3.1.1 on 2021-01-12 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournment', '0011_auto_20201215_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='loc',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='PGN File Location'),
        ),
        migrations.AlterField(
            model_name='document',
            name='rounds',
            field=models.CharField(blank=True, max_length=125, null=True),
        ),
    ]
