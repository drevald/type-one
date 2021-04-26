# Generated by Django 3.0.5 on 2021-04-08 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0008_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='meal',
        ),
        migrations.AddField(
            model_name='photo',
            name='record',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='records.Record'),
        ),
    ]