# Generated by Django 3.2.16 on 2022-12-08 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20221208_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='addressline1',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='addressline2',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='city',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='postalCode',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='profileImage',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='province',
        ),
    ]
