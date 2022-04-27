# Generated by Django 3.0.5 on 2022-04-26 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220426_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='glucose_level_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.GlucoseUnit'),
        ),
        migrations.AlterField(
            model_name='user',
            name='long_acting_insulin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='long_insulin_users', to='core.Insulin'),
        ),
        migrations.AlterField(
            model_name='user',
            name='rapid_acting_insulin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rapid_insulin_users', to='core.Insulin'),
        ),
    ]
