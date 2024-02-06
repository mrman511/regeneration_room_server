# Generated by Django 4.2.8 on 2024-02-06 07:25

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import operating_hours.models


class Migration(migrations.Migration):

    dependencies = [
        ('operating_hours', '0003_holidayhours'),
    ]

    operations = [
        migrations.RenameField(
            model_name='holidayhours',
            old_name='day_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='holidayhours',
            name='operating_hours',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='holiday_hours', to='operating_hours.operatinghours'),
        ),
        migrations.AlterField(
            model_name='operatinghours',
            name='closing_hours',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(blank=True, null=True), default=operating_hours.models.OperatingHours.default_closing_hours, size=7),
        ),
        migrations.AlterField(
            model_name='operatinghours',
            name='opening_hours',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TimeField(blank=True, null=True), default=operating_hours.models.OperatingHours.default_opening_hours, size=7),
        ),
    ]