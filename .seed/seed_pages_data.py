#!/usr/bin/env python
"""
Seed script for Management, About, and Services pages
Populates database with professional content for Propertism Realty Advisors
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from content.models import (
    CompanyInfo,
    TeamMember,
    Service,
    CoreValue,
    Statistic,
    ExpertiseArea
)


def seed_company_about():
    """Update CompanyInfo with About page content"""
    print("Updating Company About information...")
    
    company = CompanyInfo.objects.first()
    if not company:
        print("❌ No CompanyInfo found. Run init_data.py first.")
        return
    
    company.about_mission = (
        "At Propertism Realty Advisors LLP, we bridge the distance between NRI property owners "
        "and their investments in India. Our mission is to provide comprehensive property management "
        "services that give you peace of mind, knowing your assets are professionally managed, "
        "maintained, and optimized for returns."
    )
    
    company.about_description = (
        "We are a team of professionals excelled in various prospects, driven by technology-enabled "
        "solutions. Our passion for exploration and learning led us to assist property owners who are "
        "far from their investments. We understand that owning property is vital, and the absence of "
        "on-ground presence can be a hindrance. That's why we provide end-to-end property management "
        "services, from tenant management to maintenance, ensuring your property is in safe hands."
    )
    
    company.save()
    print("✓ Company About information updated")


def seed_statistics():
    """Create or update statistics"""
    print("\nSeeding Statistics...")
    
    stats_data = [
        {"label": "Properties Managed", "value": "500+", "order": 1},
        {"label": "Satisfied NRI Clients", "value": "1200+", "order": 2},
        {"label": "Years of Experience", "value": "15+", "order": 3},
        {"label": "Cities Covered", "value": "5+", "order": 4},
    ]
    
    Statistic.objects.all().delete()
    
    for stat_data in stats_data:
        stat = Statistic.objects.create(**stat_data, is_active=True)
        print(f"  ✓ Created: {stat.value} {stat.label}")


def seed_core_values():
    """Create or update core values"""
    print("\nSeeding Core Values...")
    
    values_data = [
        {
            "title": "Trust & Transparency",
            "description": "We believe in complete transparency in all our dealings. Regular updates, detailed reports, and honest communication form the foundation of our service. Your trust is our most valuable asset.",
            "icon": "✓",
            "order": 1
        },
        {
            "title": "Professional Excellence",
            "description": "We strive for excellence in every aspect of property management, from tenant selection to maintenance coordination. Our team ensures your property receives the highest standard of care.",
            "icon": "★",
            "order": 2
        },
        {
            "title": "Reliability & Accountability",
            "description": "Count on us to be there when you need us. Our dedicated team provides consistent, dependable service with clear accountability at every step of property management.",
            "icon": "◆",
            "order": 3
        },
        {
            "title": "Technology-Driven Solutions",
            "description": "We leverage modern technology to provide real-time updates, digital documentation, and seamless communication, making property management effortless for NRI owners.",
            "icon": "⚡",
            "order": 4
        },
    ]
    
    CoreValue.objects.all().delete()
    
    for value_data in values_data:
        value = CoreValue.objects.create(**value_data, is_active=True)
        print(f"  ✓ Created: {value.title}")


def seed_services():
    """Create or update services"""
    print("\nSeeding Services...")
    
    services_data = [
        {
            "title": "Real Estate Buy & Sell Assistance",
            "short_description": "Expert guidance for property transactions in Chennai and surrounding areas.",
            "full_description": (
                "We assist clients interested in investing in property or selling their assets at profitable prices. "
                "Our team provides comprehensive market analysis, property valuation, legal documentation support, "
                "and negotiation assistance. Whether you're buying your first property or expanding your portfolio, "
                "we ensure smooth transactions with complete transparency."
            ),
            "features": (
                "Property search and shortlisting\n"
                "Market analysis and valuation\n"
                "Legal documentation support\n"
                "Negotiation assistance\n"
                "Post-sale support"
            ),
            "icon": "🏠",
            "order": 1
        },
        {
            "title": "Rental & Apartment Maintenance",
            "short_description": "Complete tenant management and property maintenance services for NRI owners.",
            "full_description": (
                "Tenant management is one of our core strengths. We handle everything from tenant screening to "
                "rent collection and property maintenance. Our team conducts periodic property visits, manages "
                "rental agreements, ensures timely rent deposits, and provides detailed monthly reports. "
                "We see from the customer's perspective and deliver the best services."
            ),
            "features": (
                "Tenant screening and verification\n"
                "Rental agreement management\n"
                "Monthly rent collection and deposits\n"
                "Regular property inspections\n"
                "Maintenance coordination\n"
                "Detailed monthly reports"
            ),
            "icon": "🔑",
            "order": 2
        },
        {
            "title": "Industrial Land Services",
            "short_description": "Specialized services for industrial land acquisition and development.",
            "full_description": (
                "Propertism assists with industrial land requirements for manufacturing units and industrial plants. "
                "We provide vast area options based on your requirement analysis, handle sale and purchase transactions, "
                "coordinate with government authorities for approvals, and ensure compliance with industrial regulations. "
                "Our expertise helps businesses establish their manufacturing presence efficiently."
            ),
            "features": (
                "Industrial land search and analysis\n"
                "Government approval coordination\n"
                "Compliance and documentation\n"
                "Site development consultation\n"
                "Transaction management"
            ),
            "icon": "🏭",
            "order": 3
        },
        {
            "title": "Property Investment Consultation",
            "short_description": "Strategic advice for long-term property investments and portfolio management.",
            "full_description": (
                "Invest right and manage your assets with ease. Our consultation services help you make informed "
                "decisions about property investments in Chennai's growing real estate market. We provide market "
                "insights, ROI analysis, portfolio diversification strategies, and ongoing investment monitoring. "
                "Talk to us for expert advice on building your property portfolio."
            ),
            "features": (
                "Market trend analysis\n"
                "ROI projections\n"
                "Portfolio diversification advice\n"
                "Investment risk assessment\n"
                "Long-term wealth planning"
            ),
            "icon": "📊",
            "order": 4
        },
    ]
    
    Service.objects.all().delete()
    
    for service_data in services_data:
        service = Service.objects.create(**service_data, is_active=True)
        print(f"  ✓ Created: {service.title}")


def seed_team_members():
    """Create or update team members"""
    print("\nSeeding Team Members...")
    
    team_data = [
        {
            "name": "Vijayakumar Ramasamy",
            "role": "Managing Director",
            "department": "Leadership & Strategy",
            "bio": (
                "With over 15 years of experience in Chennai real estate market, Vijayakumar leads "
                "Propertism's strategic vision and client relationships. His expertise in NRI property "
                "management and deep understanding of market dynamics has helped hundreds of clients "
                "successfully manage their property investments from abroad."
            ),
            "expertise": "Real Estate Strategy, NRI Services, Market Analysis, Client Relations",
            "order": 1
        },
        {
            "name": "Priya Sundaram",
            "role": "Head of Operations",
            "department": "Operations & Tenant Management",
            "bio": (
                "Priya oversees all property operations and tenant management services. With a background "
                "in property management and customer service, she ensures seamless coordination between "
                "property owners, tenants, and maintenance teams. Her attention to detail and proactive "
                "approach has earned consistent client satisfaction."
            ),
            "expertise": "Tenant Management, Property Operations, Maintenance Coordination, Customer Service",
            "order": 2
        },
        {
            "name": "Rajesh Kumar",
            "role": "Senior Property Consultant",
            "department": "Sales & Acquisitions",
            "bio": (
                "Rajesh specializes in property transactions and investment advisory. His extensive network "
                "in Chennai's real estate sector and negotiation skills help clients secure the best deals. "
                "He has successfully facilitated over 200 property transactions, ranging from residential "
                "apartments to industrial land acquisitions."
            ),
            "expertise": "Property Sales, Investment Advisory, Market Valuation, Negotiation",
            "order": 3
        },
        {
            "name": "Lakshmi Venkatesh",
            "role": "Client Relations Manager",
            "department": "Client Services & Support",
            "bio": (
                "Lakshmi is the primary point of contact for NRI clients, ensuring clear communication "
                "and timely updates. Her multilingual capabilities and understanding of cross-cultural "
                "communication help bridge the distance between clients abroad and their properties in India. "
                "She coordinates all client reporting and feedback mechanisms."
            ),
            "expertise": "Client Communication, Reporting, Cross-cultural Relations, Problem Resolution",
            "order": 4
        },
    ]
    
    TeamMember.objects.all().delete()
    
    for member_data in team_data:
        member = TeamMember.objects.create(**member_data, is_active=True)
        print(f"  ✓ Created: {member.name} - {member.role}")


def seed_expertise_areas():
    """Create or update expertise areas"""
    print("\nSeeding Expertise Areas...")
    
    expertise_data = [
        {
            "title": "NRI Property Management",
            "description": (
                "Specialized services for Non-Resident Indians managing properties in Chennai. "
                "We understand the unique challenges of managing property from abroad and provide "
                "comprehensive solutions with regular updates and transparent reporting."
            ),
            "order": 1
        },
        {
            "title": "Tenant Screening & Management",
            "description": (
                "Thorough tenant verification, background checks, and ongoing tenant relationship management. "
                "We ensure reliable tenants and handle all aspects of rental agreements and rent collection."
            ),
            "order": 2
        },
        {
            "title": "Property Maintenance",
            "description": (
                "Regular property inspections, preventive maintenance, and emergency repairs coordination. "
                "We maintain your property as if it were our own, ensuring long-term asset preservation."
            ),
            "order": 3
        },
        {
            "title": "Real Estate Transactions",
            "description": (
                "End-to-end support for buying and selling properties, including market analysis, "
                "legal documentation, and negotiation. Our expertise ensures smooth and profitable transactions."
            ),
            "order": 4
        },
        {
            "title": "Industrial Land Advisory",
            "description": (
                "Specialized knowledge in industrial land acquisition, government approvals, and compliance. "
                "We help businesses establish manufacturing units with proper site selection and documentation."
            ),
            "order": 5
        },
        {
            "title": "Investment Consultation",
            "description": (
                "Strategic advice on property investments, portfolio diversification, and ROI optimization. "
                "We help clients build wealth through smart real estate investments in Chennai's growing market."
            ),
            "order": 6
        },
    ]
    
    ExpertiseArea.objects.all().delete()
    
    for expertise in expertise_data:
        area = ExpertiseArea.objects.create(**expertise, is_active=True)
        print(f"  ✓ Created: {area.title}")


def main():
    """Run all seeding functions"""
    print("=" * 60)
    print("SEEDING PAGES DATA FOR PROPERTISM REALTY ADVISORS")
    print("=" * 60)
    
    try:
        seed_company_about()
        seed_statistics()
        seed_core_values()
        seed_services()
        seed_team_members()
        seed_expertise_areas()
        
        print("\n" + "=" * 60)
        print("✓ ALL DATA SEEDED SUCCESSFULLY!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Visit http://localhost:8000/management/ to see team members")
        print("2. Visit http://localhost:8000/about/ to see company info")
        print("3. Visit http://localhost:8000/services/ to see services")
        print("\nTo manage content, visit: http://localhost:8000/admin/")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
