from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0011_herobackgroundimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="companyinfo",
            name="about_primary_cta_text",
            field=models.CharField(default="Meet Management", max_length=80),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="about_secondary_cta_text",
            field=models.CharField(default="Request a callback", max_length=80),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="about_section_eyebrow",
            field=models.CharField(default="About", max_length=100),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="about_section_title",
            field=models.CharField(default="Property support for owners living abroad.", max_length=200),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="blog_section_description",
            field=models.TextField(default="Short, practical guidance around reporting, rentals, maintenance, and ownership decisions in Chennai."),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="blog_section_eyebrow",
            field=models.CharField(default="Insights", max_length=100),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="blog_section_title",
            field=models.CharField(default="Useful updates for owners managing from abroad.", max_length=220),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="chat_sending_text",
            field=models.CharField(default="Sending...", max_length=40),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="chat_submit_text",
            field=models.CharField(default="Send", max_length=40),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="chat_success_message",
            field=models.TextField(default="Thanks for reaching out. We'll get back to you within 24 hours."),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="chat_success_title",
            field=models.CharField(default="Message sent!", max_length=120),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="chat_window_subtitle",
            field=models.CharField(default="We'll get back to you soon", max_length=160),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="chat_window_title",
            field=models.CharField(default="Leave a message", max_length=120),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="contact_form_submit_text",
            field=models.CharField(default="Send My Request", max_length=80),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="contact_primary_cta_text",
            field=models.CharField(default="Talk to Us", max_length=80),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="contact_section_description",
            field=models.TextField(default="Whether you're managing from abroad or looking to invest in Chennai, we're here to help. Share your requirements and we'll provide expert guidance."),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="contact_section_eyebrow",
            field=models.CharField(default="Get in Touch", max_length=100),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="contact_section_title",
            field=models.CharField(default="Let's discuss your property needs", max_length=200),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="footer_newsletter_button_text",
            field=models.CharField(default="Subscribe", max_length=80),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="footer_newsletter_description",
            field=models.TextField(default="Subscribe for market insights, NRI ownership updates, and new property opportunities."),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="footer_newsletter_heading",
            field=models.CharField(default="Stay Updated", max_length=120),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="footer_services_heading",
            field=models.CharField(default="Service Coverage", max_length=120),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="management_section_description",
            field=models.TextField(default="Practical accountability on the ground matters more than generic advisory. The management team is structured around execution, reporting, and decision support for owners abroad."),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="management_section_eyebrow",
            field=models.CharField(default="Management", max_length=100),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="management_section_title",
            field=models.CharField(default="One team coordinating owners, tenants, vendors, and follow-through.", max_length=220),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="proof_section_eyebrow",
            field=models.CharField(default="Why Owners Stay With Us", max_length=100),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="proof_section_title",
            field=models.CharField(default="Clear updates, reliable follow-through, and local execution.", max_length=220),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="properties_section_cta_text",
            field=models.CharField(default="Request Property Shortlist", max_length=80),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="properties_section_subtitle",
            field=models.TextField(default="Handpicked premium properties perfect for investment"),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="properties_section_title",
            field=models.CharField(default="Featured Properties for NRIs", max_length=200),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="services_card_cta_text",
            field=models.CharField(default="Discuss this service", max_length=80),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="services_section_description",
            field=models.TextField(default="Buy, rent, maintain, and monitor property with one coordinated team in Chennai."),
        ),
        migrations.AddField(
            model_name="companyinfo",
            name="services_section_title",
            field=models.CharField(default="Services built for NRI ownership", max_length=200),
        ),
    ]
