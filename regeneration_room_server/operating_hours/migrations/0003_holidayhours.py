# Generated by Django 4.2.8 on 2024-02-05 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operating_hours', '0002_alter_operatinghours_closing_hours_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HolidayHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_name', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('opening_hours', models.TimeField(blank=True, null=True)),
                ('closed_hours', models.TimeField(blank=True, null=True)),
                ('is_open', models.BooleanField(default=True)),
                ('operating_hours', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='operating_hours.operatinghours')),
            ],
        ),
    ]