# Generated by Django 3.2.16 on 2023-01-17 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20221213_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogsection',
            name='wordcount',
            field=models.CharField(max_length=200, null=True),
        ),
    ]