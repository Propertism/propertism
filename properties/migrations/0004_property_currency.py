from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0003_merge_20260308_0945"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="currency",
            field=models.CharField(
                choices=[("INR", "Indian Rupee"), ("USD", "US Dollar")],
                default="INR",
                max_length=3,
            ),
        ),
    ]
