# Generated by Django 4.2 on 2024-02-26 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aws_app', '0004_remove_databasespecifications_max_iops_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computespecifications',
            name='cloud_service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='compute_specs', to='aws_app.cloudservice'),
        ),
    ]