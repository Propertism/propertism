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
        ('properties', '0005_inquiry_indexes'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.RunPython(populate_slugs, reverse_slugs),
        migrations.AlterField(
            model_name='property',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
