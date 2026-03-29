# Generated migration to make subject and phone optional in ContactMessage

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='subject',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='contactmessage',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
