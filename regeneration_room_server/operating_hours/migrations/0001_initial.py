# Generated by Django 4.2.8 on 2024-02-05 23:40

import django.contrib.postgres.fields
from django.db import migrations, models
import operating_hours.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OperatingHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening_hours', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, null=True), size=7)),
                ('closing_hours', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, null=True), size=7)),
                ('days_closed', django.contrib.postgres.fields.ArrayField(base_field=models.DateField(blank=True, null=True), blank=True, null=True, size=None)),
                ('weekdays_open', django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(default=True), default=operating_hours.models.OperatingHours.default_days_open, size=7)),
            ],
        ),
    ]
