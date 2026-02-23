"""
Seed script to populate content from propertism.com
Run with: python manage.py shell < seed_content.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from content.models import (
    CompanyInfo, Statistic, Service, CoreValue, TeamMember,
    ExpertiseArea
)

def seed_company_info():
    """Seed company information"""
    company, created = CompanyInfo.objects.get_or_create(
        id=1,
        defaults={
            'company_name': 'Propertism Realty Advisors LLP',
            'tagline': 'We manage your property and resources when you are far from the nation',
            'about_mission': 'At Propertism Realty Advisors LLP, we specialize in providing comprehensive property management and real estate services for Non-Resident Indians (NRIs) and global investors.',
            'about_description': 'We are a team of professionals excelled enough in various prospects, who quench our thirst with technology-driven solutions. Our passion and interest in exploration and learning, lead one to the other, settling with a lightening thought to assist the Fellowship of properties.',
            
            # India Office
            'india_office_address': 'No. 30, 3rd Floor, SSR Pankajam Towers, Arunachalam Road, Saligramam',
            'india_office_city': 'Chennai',
            'india_office_state': 'Tamil Nadu',
            'india_office_pincode': '600093',
            'india_phone_1': '+91 86670 20798',
            'india_phone_2': '+91 98412 01930',
            'india_phone_3': '+91 98418 44452',
            
            # US Office
            'us_office_address': '46 Berkshire Pl',
            'us_office_city': 'Hackensack',
            'us_office_state': 'NJ',
            'us_office_zipcode': '07601',
            'us_phone': '+1 518 409 3485',
            
            # Contact
            'email': 'info@propertism.com',
            
            # Social Media
            'facebook_url': 'https://facebook.com/propertism',
            'twitter_url': 'https://twitter.com/propertism',
            'linkedin_url': 'https://linkedin.com/company/propertism',
            
            # Business Hours
            'business_hours': 'Monday - Saturday: 9:00 AM - 6:00 PM IST',
        }
    )
    
    if created:
        print("✅ Company information created")
    else:
        print("ℹ️  Company information already exists")
    
    return company


def seed_statistics():
    """Seed company statistics"""
    stats = [
        {'label': 'Properties Managed', 'value': '500+', 'order': 1},
        {'label': 'Satisfied Clients', 'value': '1200+', 'order': 2},
        {'label': 'Years of Experience', 'value': '15+', 'order': 3},
    ]
    
    for stat_data in stats:
        stat, created = Statistic.objects.get_or_create(
            label=stat_data['label'],
            defaults=stat_data
        )
        if created:
            print(f"✅ Statistic created: {stat}")


def seed_services():
    """Seed services from propertism.com"""
    services = [
        {
            'title': 'Real Estate Buy & Sell',
            'slug': 'real-estate-buy-sell',
            'short_description': 'We assist in buying and selling properties, to clients who are interested in investing in a property or who want to sell their plot at a profitable price.',
            'full_description': 'Expert guidance for buying and selling residential and commercial properties in Chennai. We handle everything from property search to legal documentation, ensuring a smooth transaction process.',
            'icon': '🏢',
            'order': 1,
            'features': '''Property valuation and market analysis
Legal documentation and verification
Negotiation and deal closure
Title search and clearance
Registration assistance
Post-sale support''',
        },
        {
            'title': 'Rental & Maintenance',
            'slug': 'rental-maintenance',
            'short_description': 'Tenant management is one of the best colored feathers in our hat. We see from the Customer\'s point and give them the best services. We take periodic visits to your place and take care of rental cheques deposits, reports.',
            'full_description': 'Complete property management services for NRIs. We find reliable tenants, collect rent, and maintain your property as if it were our own.',
            'icon': '🔑',
            'order': 2,
            'features': '''Tenant screening and verification
Rent collection and remittance
Regular property inspections
Maintenance and repairs
Utility bill management
Monthly reports and updates''',
        },
        {
            'title': 'Industrial Land Services',
            'slug': 'industrial-land-services',
            'short_description': 'Propertism also helps with Industrial land requirements. Sale and purchase of the land required for Industry plants, according to the requirement analysis.',
            'full_description': 'Specialized services for industrial land acquisition, development, and management. Perfect for businesses looking to establish or expand operations in Chennai.',
            'icon': '🏭',
            'order': 3,
            'features': '''Industrial land identification
Zoning and compliance verification
Development planning
Government approvals assistance
Infrastructure coordination
Investment advisory''',
        },
    ]
    
    for service_data in services:
        service, created = Service.objects.get_or_create(
            slug=service_data['slug'],
            defaults=service_data
        )
        if created:
            print(f"✅ Service created: {service}")


def seed_core_values():
    """Seed core values"""
    values = [
        {
            'title': 'Trust & Transparency',
            'description': 'We believe in complete transparency in all our dealings. Regular updates, detailed reports, and honest communication are the foundation of our service.',
            'icon': '✓',
            'order': 1,
        },
        {
            'title': 'Excellence',
            'description': 'We strive for excellence in every aspect of property management, from tenant selection to maintenance, ensuring your property is in the best hands.',
            'icon': '★',
            'order': 2,
        },
        {
            'title': 'Reliability',
            'description': 'Count on us to be there when you need us. Our team is dedicated to providing consistent, dependable service that you can trust.',
            'icon': '◆',
            'order': 3,
        },
    ]
    
    for value_data in values:
        value, created = CoreValue.objects.get_or_create(
            title=value_data['title'],
            defaults=value_data
        )
        if created:
            print(f"✅ Core value created: {value}")


def seed_team_members():
    """Seed team members"""
    members = [
        {
            'name': 'Managing Director',
            'role': 'Managing Director',
            'department': 'Leadership & Strategy',
            'bio': 'With over 15 years of experience in real estate and property management, our Managing Director leads the strategic vision of Propertism, ensuring excellence in every client interaction.',
            'order': 1,
            'expertise': 'Real Estate Strategy, NRI Services, Business Development',
        },
        {
            'name': 'Operations Head',
            'role': 'Operations Head',
            'department': 'Property Management',
            'bio': 'Overseeing day-to-day operations, our Operations Head ensures that every property under our management receives meticulous attention and professional care.',
            'order': 2,
            'expertise': 'Operations Management, Tenant Relations, Maintenance',
        },
        {
            'name': 'Legal Advisor',
            'role': 'Legal Advisor',
            'department': 'Legal & Compliance',
            'bio': 'Our Legal Advisor ensures all transactions and property management activities comply with Indian real estate laws and regulations, protecting your interests.',
            'order': 3,
            'expertise': 'Property Law, Documentation, Compliance',
        },
        {
            'name': 'Client Relations Manager',
            'role': 'Client Relations Manager',
            'department': 'Client Services',
            'bio': 'Dedicated to maintaining strong relationships with our NRI clients, ensuring clear communication and prompt resolution of all queries and concerns.',
            'order': 4,
            'expertise': 'Client Communication, NRI Support, Reporting',
        },
    ]
    
    for member_data in members:
        member, created = TeamMember.objects.get_or_create(
            role=member_data['role'],
            defaults=member_data
        )
        if created:
            print(f"✅ Team member created: {member}")


def seed_expertise_areas():
    """Seed collective expertise areas"""
    areas = [
        {
            'title': 'Real Estate Transactions',
            'description': 'Comprehensive knowledge of Chennai real estate market, property valuation, and transaction management',
            'order': 1,
        },
        {
            'title': 'Property Management',
            'description': 'Expert handling of rental properties, tenant management, and property maintenance services',
            'order': 2,
        },
        {
            'title': 'Legal Compliance',
            'description': 'In-depth understanding of property laws, documentation, and regulatory requirements',
            'order': 3,
        },
        {
            'title': 'NRI Services',
            'description': 'Specialized support for Non-Resident Indians managing properties from abroad',
            'order': 4,
        },
        {
            'title': 'Industrial Land',
            'description': 'Expertise in industrial land acquisition, zoning, and development projects',
            'order': 5,
        },
        {
            'title': 'Investment Advisory',
            'description': 'Strategic guidance on property investments and portfolio management',
            'order': 6,
        },
    ]
    
    for area_data in areas:
        area, created = ExpertiseArea.objects.get_or_create(
            title=area_data['title'],
            defaults=area_data
        )
        if created:
            print(f"✅ Expertise area created: {area}")


def main():
    """Run all seed functions"""
    print("\n🌱 Starting content seeding from propertism.com...\n")
    
    seed_company_info()
    seed_statistics()
    seed_services()
    seed_core_values()
    seed_team_members()
    seed_expertise_areas()
    
    print("\n✅ Content seeding completed!\n")
    print("📊 Summary:")
    print(f"   - Company Info: {CompanyInfo.objects.count()}")
    print(f"   - Statistics: {Statistic.objects.count()}")
    print(f"   - Services: {Service.objects.count()}")
    print(f"   - Core Values: {CoreValue.objects.count()}")
    print(f"   - Team Members: {TeamMember.objects.count()}")
    print(f"   - Expertise Areas: {ExpertiseArea.objects.count()}")
    print("\n🎯 Next: Update templates to use this data from Django admin\n")


if __name__ == '__main__':
    main()
