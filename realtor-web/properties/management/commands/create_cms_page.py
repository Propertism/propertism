from django.core.management.base import BaseCommand
from cms.api import create_page


class Command(BaseCommand):
    help = 'Create CMS page for Properties React SPA'

    def handle(self, *args, **options):
        try:
            # Create the page
            page = create_page(
                title='Properties',
                template='properties/cms_app.html',
                language='en',
                slug='properties',
                published=True,
                apphook='PropertiesAppHook',
                apphook_namespace='properties_spa',
            )

            self.stdout.write(self.style.SUCCESS(f'✅ Successfully created Properties page!'))
            self.stdout.write(self.style.SUCCESS(f'   Page ID: {page.pk}'))
            self.stdout.write(self.style.SUCCESS(f'   URL: http://localhost:8000/en/properties/'))
            self.stdout.write(self.style.SUCCESS(f'   Template: properties/cms_app.html'))
            self.stdout.write(self.style.SUCCESS(f'   AppHook: PropertiesAppHook'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating page: {str(e)}'))
            self.stdout.write(self.style.WARNING('   Page may already exist. Try visiting: http://localhost:8000/en/properties/'))
