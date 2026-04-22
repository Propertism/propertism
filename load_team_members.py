#!/usr/bin/env python
"""
One-time script to load team members into production database.
Run this manually: python load_team_members.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from content.models import TeamMember

def load_team_members():
    """Load the 3 team members if they don't already exist"""
    
    team_data = [
        {
            'name': 'Mr. Tamilselvan',
            'slug': 'mr-tamilselvan',
            'role': 'Managing Partner',
            'department': 'Property Acquisition & Management',
            'bio': "Mr. Tamilselvan possesses rich domain knowledge with respect to land and properties. His experience is about 15 years in this field. His fields of excellence include land acquisitions with varied experience from top companies like Sri Kumaran Properties and Builders where he was the managing partner. Everonn Education Limited is his next company where he worked on the same vertical that includes property acquisition. He was the regional manager for the property acquisition vertical at People Combine. Now, he is all set with Propertism to give his fullest of all experience to serve clients for property management. His skills include land acquisitions, property managements, building contract managements, property development, negotiations, etc. which encompasses the property business coupled with management tactics. He is a MBA grad from Symbiosis Centre of Distance Learning.",
            'photo': 'team/ics-11.png',
            'order': 1,
            'is_active': True,
            'expertise': 'Land Acquisitions, Property Management, Building Contract Management, Property Development, Negotiations'
        },
        {
            'name': 'Mr. Lawrence Manickam',
            'slug': 'mr-lawrence-manickam',
            'role': 'Technology Partner',
            'department': 'Technology & Innovation',
            'bio': "Propertism involves cutting-edge technologies, and Lawrence has 15 years of experience in IT industry. Right now, he is based out of New York, who owns Tecneto - http://www.tecneto.com/ and Realneeds - www.realneeds.org located in India and NY. He kick-started his career as a programmer with iGateGlobalSolutions and has considerable experience in Data warehousing domain. His skills includes much experiments with business intelligence, business objects, and a lot more; that enhanced his skillset. He is one of the pillars of Propertism who will be supporting on every strand with his vast knowledge. He possesses an Engineering degree from Bharathidasan University.",
            'photo': 'team/ics-11.png',
            'order': 2,
            'is_active': True,
            'expertise': 'Business Intelligence, Data Warehousing, Technology Strategy, Software Development'
        },
        {
            'name': 'Mr. Raju Packianathan',
            'slug': 'mr-raju-packianathan',
            'role': 'Co-Founder',
            'department': 'Business Strategy & Entrepreneurship',
            'bio': "Raju is the first-generation entrepreneur, who is the co-founder of Quadruple Group of Companies - www.quadruplegroup.com formed in 2008 and is one of the leading IT firms with 100+ employees. Raju has about 18 years of experience with information technology and entrepreneurial skills. He firmly believes that everything is possible with technology and pitches in with ideas to explore with technology alignment. His skills encircle the well-known tactics for business strategy planning, entrepreneur skillset, and customer engagement activities. He holds an MBA degree with marketing specialization from Madurai Kamaraj University.",
            'photo': 'team/ics-11.png',
            'order': 3,
            'is_active': True,
            'expertise': 'Business Strategy Planning, Entrepreneurship, Customer Engagement, Technology Alignment'
        }
    ]
    
    created_count = 0
    skipped_count = 0
    
    for data in team_data:
        # Check if member already exists by slug
        if TeamMember.objects.filter(slug=data['slug']).exists():
            print(f"⏭️  Skipped: {data['name']} (already exists)")
            skipped_count += 1
        else:
            TeamMember.objects.create(**data)
            print(f"✅ Created: {data['name']}")
            created_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   Created: {created_count}")
    print(f"   Skipped: {skipped_count}")
    print(f"   Total: {created_count + skipped_count}")

if __name__ == '__main__':
    print("🚀 Loading team members...\n")
    load_team_members()
    print("\n✅ Done!")
