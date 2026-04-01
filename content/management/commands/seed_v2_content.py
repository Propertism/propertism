from django.core.management.base import BaseCommand
from content.models import CompanyInfo, TeamMember, Service, CoreValue, Statistic, ExpertiseArea

class Command(BaseCommand):
    help = 'Seed real content from legacy propertism.com site'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('SEEDING REAL PROPERTISM CONTENT')
        self.stdout.write('=' * 60)
        
        # Update Company Info with real data
        self.stdout.write('\nUpdating Company Info...')
        company = CompanyInfo.objects.first()
        if company:
            company.hero_eyebrow = 'Propertism Realty Advisors'
            company.hero_title = 'NRI Property Management Services In Chennai, India'
            company.hero_description = 'We manage your property and resources, when you are far from the nation'
            company.about_description = 'We are a team of professionals excelled enough in various prospects, who quench our thirst with technology-driven solution. Our passion and interest in exploration and learning, lead one to the other, settling with a lightening thought to assist the Fellowship of properties.'
            
            # Real office addresses
            company.india_office_address = 'No. 30, 3rd Floor, SSR Pankajam Towers, Arunachalam Road, Saligramam'
            company.india_office_city = 'Chennai'
            company.india_office_state = 'Tamil Nadu'
            company.india_office_zip = '600093'
            company.india_phone_1 = '+91 86670 20798'
            company.india_phone_2 = '+91 98412 01930'
            
            company.us_office_address = '46 Berkshire Pl'
            company.us_office_city = 'Hackensack'
            company.us_office_state = 'NJ'
            company.us_office_zip = '07601'
            company.us_phone_1 = '518 409 3485'
            
            company.save()
            self.stdout.write(self.style.SUCCESS('✓ Company info updated with real data'))
        
        # Only clear and seed if no team members exist (bootstrap only)
        if TeamMember.objects.exists():
            self.stdout.write(self.style.WARNING('⚠ Data already exists, skipping seed to preserve content'))
            return
        
        self.stdout.write('\nSeeding initial data...')
        
        # Seed Real Team Members from propertism.com
        self.stdout.write('\nSeeding Real Team Members...')
        team_members = [
            {
                'name': 'Mr. Tamilselvan',
                'role': 'Managing Partner',
                'department': 'Property Acquisition & Management',
                'bio': '''Mr. Tamilselvan possesses rich domain knowledge with respect to land and properties. His experience is about 15 years in this field. His fields of excellence include land acquisitions with varied experience from top companies like Sri Kumaran Properties and Builders where he was the managing partner. Everonn Education Limited, is his next company where he worked on the same vertical that includes property acquisition. He was the regional manager for the property acquisition vertical at 'People combine'. Now, he is all set with Propertism to give his fullest of all experience to serve clients for property management.

His skills include land acquisitions, property managements, building contract managements, property development, negotiations, etc. which encompasses the property business coupled with management tactics.

He is a MBA grad from Symbiosis Centre of Distance Learning.''',
                'expertise': 'Land Acquisitions, Property Management, Building Contract Management, Property Development, Negotiations',
                'is_active': True,
                'order': 1
            },
            {
                'name': 'Mr. Lawrence Manickam',
                'role': 'Technology Partner',
                'department': 'Technology & Innovation',
                'bio': '''Propertism involves cutting-edge technologies, and Lawrence has 15 years of experience in IT industry. Right now, he is based out of New York, who owns Tecneto - http://www.tecneto.com/ and Realneeds - www.realneeds.org located in India and NY. He kick-started his career as a programmer with iGateGlobalSolutions and has considerable experience in Data warehousing domain.

His skills includes much experiments with business intelligence, business objects, and a lot more; that enhanced his skillset. He is one of the pillars of Propertism who will be supporting on every strand with his vast knowledge.

He possesses an Engineering degree from Bharathidasan University.''',
                'expertise': 'Business Intelligence, Data Warehousing, Technology Strategy, Software Development',
                'is_active': True,
                'order': 2
            },
            {
                'name': 'Mr. Raju Packianathan',
                'role': 'Co-Founder',
                'department': 'Business Strategy & Entrepreneurship',
                'bio': '''Raju is the first-generation entrepreneur, who is the co-founder of Quadruple Group of Companies – www.quadruplegroup.com formed in 2008 and is one of the leading IT firms with 100+ employees. Raju has about 18 years of experience with information technology and entrepreneurial skills. He firmly believes that everything is possible with technology and pitches in with ideas to explore with technology alignment.

His skills encircle the well-renowned tactics for the business strategy planning, entrepreneur skillset, and customer engagement activities.

He holds an MBA degree with marketing specialization from Madurai Kamaraj University.''',
                'expertise': 'Business Strategy Planning, Entrepreneurship, Customer Engagement, Technology Alignment',
                'is_active': True,
                'order': 3
            }
        ]
        
        for member_data in team_members:
            TeamMember.objects.create(**member_data)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(team_members)} real team members'))
        
        # Seed Real Services from propertism.com
        self.stdout.write('\nSeeding Real Services...')
        services = [
            {
                'title': 'Real Estate – Buy and Sell assistance',
                'short_description': 'We assist in buying and selling properties, to clients who are interested in investing in a property or who want to sell their plot at a profitable price.',
                'full_description': 'We assist in buying and selling properties, to clients who are interested in investing in a property or who want to sell their plot at a profitable price. Our team provides comprehensive support throughout the transaction process.',
                'is_active': True,
                'order': 1
            },
            {
                'title': 'Rental and Apartment Maintenance',
                'short_description': 'Tenant management is one of the best colored feathers in our hat, we see from the Customer\'s point and give them the best services.',
                'full_description': 'Tenant management is one of the best colored feathers in our hat, we see from the Customer\'s point and give them the best services. We take periodic visits to your place and take care of rental cheques deposits, reports.',
                'is_active': True,
                'order': 2
            },
            {
                'title': 'Industrial Land Services',
                'short_description': 'Propertism, also helps with Industrial land requirements. Sale and purchase of the land required for Industry plants.',
                'full_description': 'Propertism, also helps with Industrial land requirements. Sale and purchase of the land required for Industry plants, according to the requirement analysis.',
                'is_active': True,
                'order': 3
            }
        ]
        
        for service_data in services:
            Service.objects.create(**service_data)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(services)} real services'))
        
        # Seed Core Values (minimal, no fake data)
        self.stdout.write('\nSeeding Core Values...')
        core_values = [
            {
                'title': 'Trust & Transparency',
                'description': 'Complete transparency in all dealings with regular updates and honest communication.',
                'icon': '✓',
                'is_active': True,
                'order': 1
            },
            {
                'title': 'Professional Excellence',
                'description': 'Excellence in every aspect of property management with highest standard of care.',
                'icon': '★',
                'is_active': True,
                'order': 2
            },
            {
                'title': 'Reliability',
                'description': 'Consistent, dependable service with clear accountability at every step.',
                'icon': '◆',
                'is_active': True,
                'order': 3
            }
        ]
        
        for value_data in core_values:
            CoreValue.objects.create(**value_data)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(core_values)} core values'))
        
        # Seed Statistics (minimal, no fake numbers)
        self.stdout.write('\nSeeding Statistics...')
        statistics = [
            {
                'label': 'Years of Experience',
                'value': '15+',
                'is_active': True,
                'order': 1
            },
            {
                'label': 'Office Locations',
                'value': '2',
                'is_active': True,
                'order': 2
            }
        ]
        
        for stat_data in statistics:
            Statistic.objects.create(**stat_data)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(statistics)} statistics'))
        
        # Seed Expertise Areas (minimal)
        self.stdout.write('\nSeeding Expertise Areas...')
        expertise_areas = [
            {
                'title': 'NRI Property Management',
                'description': 'Specialized services for Non-Resident Indians managing properties in Chennai.',
                'is_active': True,
                'order': 1
            },
            {
                'title': 'Real Estate Transactions',
                'description': 'End-to-end support for buying and selling properties.',
                'is_active': True,
                'order': 2
            },
            {
                'title': 'Tenant Management',
                'description': 'Thorough tenant verification and ongoing relationship management.',
                'is_active': True,
                'order': 3
            }
        ]
        
        for expertise_data in expertise_areas:
            ExpertiseArea.objects.create(**expertise_data)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(expertise_areas)} expertise areas'))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('✓ REAL CONTENT SEEDING COMPLETED'))
        self.stdout.write('=' * 60)
