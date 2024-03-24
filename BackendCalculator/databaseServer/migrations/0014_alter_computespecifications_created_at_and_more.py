from django.db import migrations, models
from django.utils import timezone  # Import the timezone module

class Migration(migrations.Migration):

    dependencies = [
        ('databaseServer', '0013_alter_computespecifications_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computespecifications',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),  # Set a default using timezone.now
        ),
        migrations.AlterField(
            model_name='databasespecifications',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),  # Set a default using timezone.now
        ),
        migrations.AlterField(
            model_name='networkingspecifications',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),  # Set a default using timezone.now
        ),
        migrations.AlterField(
            model_name='storagespecifications',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),  # Set a default using timezone.now
        ),
    ]
