# Generated by Django 3.0.5 on 2020-04-30 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='insulin_type',
            new_name='insulin',
        ),
    ]
