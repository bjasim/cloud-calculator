# Generated by Django 4.2 on 2024-02-27 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aws_app', '0009_databasespecifications_cpu_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='databasespecifications',
            name='cloud_service',
        ),
    ]