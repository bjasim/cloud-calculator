# Generated by Django 5.0.2 on 2024-02-27 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseServer', '0008_rename_db_engine_databasespecifications_data_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='computespecifications',
            name='price_per_unit',
        ),
        migrations.AddField(
            model_name='computespecifications',
            name='unit_price',
            field=models.CharField(default='0.0', max_length=50),
        ),
    ]