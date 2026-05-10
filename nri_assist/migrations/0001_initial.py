from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NRIService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(
                    choices=[
                        ('PROPERTY_CARE', 'Property Care'),
                        ('SALE', 'Sale Assistance'),
                        ('ACQUISITION', 'Acquisition Assistance'),
                        ('PRIORITY', 'Priority Coordination'),
                    ],
                    db_index=True,
                    max_length=50,
                )),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('icon', models.CharField(blank=True, max_length=100)),
                ('metadata', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'verbose_name': 'NRI Service',
                'verbose_name_plural': 'NRI Services',
                'ordering': ['category', 'sort_order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='NRIAssistEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(
                    choices=[
                        ('PAGE_VISIT', 'NRI Assist Page Visit'),
                        ('CTA_CLICK', 'Service CTA Click'),
                        ('ADVISOR_REQUEST', 'Advisor Request Submitted'),
                        ('GOOGLE_LOGIN', 'Google Login Conversion'),
                    ],
                    db_index=True,
                    max_length=30,
                )),
                ('service_category', models.CharField(blank=True, max_length=50)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='nri_events',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'NRI Assist Event',
                'verbose_name_plural': 'NRI Assist Events',
                'ordering': ['-created_at'],
            },
        ),
    ]
