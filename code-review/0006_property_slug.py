from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_inquiry_indexes'),
    ]

    operations = [
        # One-shot cleanup for 2026-05-21 prod deploy drift.
        # The _like index was orphaned by an earlier failed deploy attempt.
        # IF EXISTS makes this a no-op on any clean environment.
        migrations.RunSQL(
            sql="DROP INDEX IF EXISTS properties_property_slug_f3b16024_like;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AddField(
            model_name='property',
            name='slug',
            field=models.SlugField(blank=True, null=True, max_length=255),
        ),
    ]
