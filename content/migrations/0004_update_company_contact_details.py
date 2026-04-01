from django.db import migrations, models


INDIA_OFFICE_ADDRESS = "No. 30, 3rd Floor\nSSR Pankajam Towers\nArunachalam Road, Saligramam"
US_OFFICE_ADDRESS = "46 Berkshire Pl"


def update_company_contact_details(apps, schema_editor):
    CompanyInfo = apps.get_model('content', 'CompanyInfo')
    CompanyInfo.objects.update(
        tagline='We manage your property and resources when you are far from the nation.',
        tagline_en='We manage your property and resources when you are far from the nation.',
        india_office_address=INDIA_OFFICE_ADDRESS,
        india_office_city='Chennai',
        india_office_state='Tamil Nadu',
        india_office_pincode='600093',
        india_phone_1='+91 86670 20798',
        india_phone_2='+91 98412 01930',
        india_phone_3='+91 98418 44452',
        us_office_address=US_OFFICE_ADDRESS,
        us_office_city='Hackensack',
        us_office_state='NJ',
        us_office_zipcode='07601',
        us_phone='+1 518 409 3485',
        email='info@propertism.com',
        business_hours='Monday - Saturday: 9:00 AM - 6:00 PM IST',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_companyinfo_hero_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='tagline',
            field=models.TextField(default='We manage your property and resources when you are far from the nation.'),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='india_office_address',
            field=models.TextField(default=INDIA_OFFICE_ADDRESS),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='india_phone_1',
            field=models.CharField(default='+91 86670 20798', max_length=20),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='india_phone_2',
            field=models.CharField(blank=True, default='+91 98412 01930', max_length=20),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='india_phone_3',
            field=models.CharField(blank=True, default='+91 98418 44452', max_length=20),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='us_office_address',
            field=models.TextField(default=US_OFFICE_ADDRESS),
        ),
        migrations.AlterField(
            model_name='companyinfo',
            name='us_phone',
            field=models.CharField(default='+1 518 409 3485', max_length=20),
        ),
        migrations.RunPython(update_company_contact_details, migrations.RunPython.noop),
    ]
