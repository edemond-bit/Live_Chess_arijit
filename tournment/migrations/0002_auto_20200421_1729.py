# Generated by Django 2.2.4 on 2020-04-21 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='endtime',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='starttime',
        ),
    ]
