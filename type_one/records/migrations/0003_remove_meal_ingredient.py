# Generated by Django 3.0.5 on 2020-05-08 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_meal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='ingredient',
        ),
    ]