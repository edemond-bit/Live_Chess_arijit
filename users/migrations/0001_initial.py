# Generated by Django 2.2.4 on 2020-04-21 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
                ('description', models.CharField(blank=True, max_length=125, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name_plural': 'Departments',
                'ordering': ['name', 'created'],
                'verbose_name': 'Department',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('signup_confirmation', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False, help_text='button to toggle employee block and unblock', verbose_name='Is Blocked')),
                ('is_deleted', models.BooleanField(default=False, help_text='button to toggle employee deleted and undelete', verbose_name='Is Deleted')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Users',
                'verbose_name': 'User',
            },
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
                ('flag', models.ImageField(blank=True, null=True, upload_to='')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name_plural': 'Nationality',
                'ordering': ['name', 'created'],
                'verbose_name': 'Nationality',
            },
        ),
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
                ('description', models.CharField(blank=True, max_length=125, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name_plural': 'Religions',
                'ordering': ['name', 'created'],
                'verbose_name': 'Religion',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
                ('description', models.CharField(blank=True, max_length=125, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name_plural': 'Roles',
                'ordering': ['name', 'created'],
                'verbose_name': 'Role',
            },
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Married', 'Married'), ('Single', 'Single'), ('Divorced', 'Divorced'), ('Widow', 'Widow'), ('Widower', 'Widower')], default='Single', max_length=10, null=True, verbose_name='Marital Status')),
                ('spouse', models.CharField(blank=True, max_length=255, null=True, verbose_name='Spouse (Fullname)')),
                ('occupation', models.CharField(blank=True, help_text='spouse occupation', max_length=125, null=True, verbose_name='Occupation')),
                ('tel', phonenumber_field.modelfields.PhoneNumberField(blank=True, default=None, help_text='Enter number with Country Code Eg. +233240000000', max_length=128, null=True, verbose_name='Spouse Phone Number (Example +233240000000)')),
                ('children', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Number of Children')),
                ('nextofkin', models.CharField(help_text='fullname of next of kin', max_length=255, null=True, verbose_name='Next of Kin')),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Phone Number of Next of Kin', max_length=128, null=True, verbose_name='Next of Kin Phone Number (Example +233240000000)')),
                ('relationship', models.CharField(choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Sister', 'Sister'), ('Brother', 'Brother'), ('Uncle', 'Uncle'), ('Aunty', 'Aunty'), ('Husband', 'Husband'), ('Wife', 'Wife'), ('Fiance', 'Fiance'), ('Cousin', 'Cousin'), ('Fiancee', 'Fiancee'), ('Niece', 'Niece'), ('Nephew', 'Nephew'), ('Son', 'Son'), ('Daughter', 'Daughter')], help_text='Who is this person to you ?', max_length=15, null=True, verbose_name='Relationship with Next of Person')),
                ('father', models.CharField(blank=True, max_length=255, null=True, verbose_name="Father's Name")),
                ('foccupation', models.CharField(blank=True, max_length=125, null=True, verbose_name="Father's Occupation")),
                ('mother', models.CharField(blank=True, max_length=255, null=True, verbose_name="Mother's Name")),
                ('moccupation', models.CharField(blank=True, max_length=125, null=True, verbose_name="Mother's Occupation")),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Employee')),
            ],
            options={
                'verbose_name_plural': 'Relationships',
                'ordering': ['created'],
                'verbose_name': 'Relationship',
            },
        ),
        migrations.CreateModel(
            name='Emergency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(help_text='who should we contact ?', max_length=255, null=True, verbose_name='Fullname')),
                ('tel', phonenumber_field.modelfields.PhoneNumberField(default='+233240000000', help_text='Enter number with Country Code Eg. +233240000000', max_length=128, verbose_name='Phone Number (Example +233240000000)')),
                ('location', models.CharField(max_length=125, null=True, verbose_name='Place of Residence')),
                ('relationship', models.CharField(choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Sister', 'Sister'), ('Brother', 'Brother'), ('Uncle', 'Uncle'), ('Aunty', 'Aunty'), ('Husband', 'Husband'), ('Wife', 'Wife'), ('Fiance', 'Fiance'), ('Cousin', 'Cousin'), ('Fiancee', 'Fiancee'), ('Niece', 'Niece'), ('Nephew', 'Nephew'), ('Son', 'Son'), ('Daughter', 'Daughter')], default='Father', help_text='Who is this person to you ?', max_length=8, null=True, verbose_name='Relationship with Person')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Employee')),
            ],
            options={
                'verbose_name_plural': 'Emergency',
                'ordering': ['-created'],
                'verbose_name': 'Emergency',
            },
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('age', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Age')),
                ('bio', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Users_Info',
                'verbose_name': 'User_Info',
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125, null=True, verbose_name='Name of Bank')),
                ('account', models.CharField(help_text='employee account number', max_length=30, null=True, verbose_name='Account Number')),
                ('branch', models.CharField(blank=True, help_text='which branch was the account issue', max_length=125, null=True, verbose_name='Branch')),
                ('salary', models.DecimalField(decimal_places=2, help_text='This is the initial salary of employee', max_digits=16, null=True, verbose_name='Starting Salary')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('employee', models.ForeignKey(help_text='select employee(s) to add bank account', null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Employee')),
            ],
            options={
                'verbose_name_plural': 'Banks',
                'ordering': ['-name', '-account'],
                'verbose_name': 'Bank',
            },
        ),
    ]
