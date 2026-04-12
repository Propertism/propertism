from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0013_landinglead"),
    ]

    operations = [
        migrations.AddField(
            model_name="landinglead",
            name="lead_score",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="landinglead",
            name="lead_category",
            field=models.CharField(default="cold", max_length=10),
        ),
        migrations.AddField(
            model_name="landinglead",
            name="expected_price_range",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="landinglead",
            name="preferred_contact_time",
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
