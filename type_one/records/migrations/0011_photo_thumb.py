# Generated by Django 3.0.5 on 2021-05-07 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0010_auto_20210408_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='thumb',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
