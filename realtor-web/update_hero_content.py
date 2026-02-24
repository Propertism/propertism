#!/usr/bin/env python
"""
Update CompanyInfo with hero section content
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtor_project.settings')
django.setup()

from content.models import CompanyInfo

def update_hero_content():
    """Update hero section content in CompanyInfo"""
    try:
        company = CompanyInfo.objects.first()
        if not company:
            print("❌ No CompanyInfo found. Please create one in Django Admin first.")
            return
        
        # Update hero fields - CORRECTED ORDER: Chennai, India
        company.hero_title = "NRI Property Management Services In Chennai, India"
        company.hero_title_en = "NRI Property Management Services In Chennai, India"
        company.hero_title_ta = "சென்னை, இந்தியாவில் NRI சொத்து மேலாண்மை சேவைகள்"
        company.hero_title_hi = "चेन्नई, भारत में NRI संपत्ति प्रबंधन सेवाएं"
        
        company.hero_description = "We manage your property and resources when you are far from the nation"
        company.hero_description_en = "We manage your property and resources when you are far from the nation"
        company.hero_description_ta = "நீங்கள் நாட்டிலிருந்து தொலைவில் இருக்கும்போது உங்கள் சொத்து மற்றும் வளங்களை நாங்கள் நிர்வகிக்கிறோம்"
        company.hero_description_hi = "जब आप देश से दूर हों तो हम आपकी संपत्ति और संसाधनों का प्रबंधन करते हैं"
        
        company.hero_eyebrow = "Propertism Realty Advisors"
        company.hero_eyebrow_en = "Propertism Realty Advisors"
        company.hero_eyebrow_ta = "சொத்துரிமை ரியல் எஸ்டேட் ஆலோசகர்கள்"
        company.hero_eyebrow_hi = "संपत्ति अधिकार रियल एस्टेट सलाहकार"
        
        company.save()
        
        print("✅ Hero content updated successfully!")
        print(f"\nHero Title (EN): {company.hero_title_en}")
        print(f"Hero Title (TA): {company.hero_title_ta}")
        print(f"Hero Title (HI): {company.hero_title_hi}")
        print(f"\nHero Description (EN): {company.hero_description_en}")
        print(f"Hero Description (TA): {company.hero_description_ta}")
        print(f"Hero Description (HI): {company.hero_description_hi}")
        print(f"\nHero Eyebrow (EN): {company.hero_eyebrow_en}")
        print(f"Hero Eyebrow (TA): {company.hero_eyebrow_ta}")
        print(f"Hero Eyebrow (HI): {company.hero_eyebrow_hi}")
        print(f"\n📝 Note: Hero image can be uploaded via Django Admin at:")
        print(f"   http://localhost:8000/admin/content/companyinfo/{company.id}/change/")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    update_hero_content()
