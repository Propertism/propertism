from django.db import migrations, models
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    Property = apps.get_model('properties', 'Property')
    seen = set()
    for prop in Property.objects.order_by('pk'):
        base = slugify(prop.title) or 'property'
        slug = base
        counter = 1
        while slug in seen:
            slug = f'{base}-{counter}'
            counter += 1
        seen.add(slug)
        prop.slug = slug
        prop.save(update_fields=['slug'])


def reverse_slugs(apps, schema_editor):
    Property = apps.get_model('properties', 'Property')
    Property.objects.update(slug='')


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_property_slug'),
    ]

    operations = [
        migrations.RunPython(populate_slugs, reverse_slugs),
        migrations.AlterField(
            model_name='property',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
