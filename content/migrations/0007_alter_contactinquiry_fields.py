# Generated migration for ContactInquiry field updates

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_companyinfo_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinquiry',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='contactinquiry',
            name='service',
            field=models.CharField(blank=True, choices=[('buy-sell', 'Real Estate Buy & Sell'), ('rental', 'Rental & Maintenance'), ('industrial', 'Industrial Land Services'), ('consultation', 'General Consultation')], max_length=20),
        ),
    ]
