from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0012_companyinfo_homepage_copy_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="LandingLead",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=200)),
                ("phone", models.CharField(max_length=20)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("property_city", models.CharField(max_length=120)),
                (
                    "property_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("apartment", "Apartment"),
                            ("villa", "Villa"),
                            ("plot", "Plot"),
                            ("commercial", "Commercial"),
                            ("industrial", "Industrial Land"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "intent_type",
                    models.CharField(
                        choices=[
                            ("sell", "Sell"),
                            ("management", "Management"),
                            ("rental", "Rental"),
                            ("maintenance", "Maintenance"),
                            ("informational", "Informational"),
                            ("buy", "Buy"),
                        ],
                        max_length=20,
                    ),
                ),
                ("geo_origin", models.CharField(blank=True, max_length=120)),
                (
                    "lead_stage",
                    models.CharField(
                        choices=[("initiated", "Initiated"), ("qualified", "Qualified")],
                        default="initiated",
                        max_length=20,
                    ),
                ),
                ("qualification_data", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Landing Lead",
                "verbose_name_plural": "Landing Leads",
                "ordering": ["-created_at"],
            },
        ),
    ]
