# Generated by Django 4.2.8 on 2024-02-06 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operating_hours', '0005_rename_closed_hours_holidayhours_closing_hours'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('num_chairs', models.IntegerField(default=5)),
            ],
        ),
    ]
