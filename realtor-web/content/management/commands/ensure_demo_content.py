"""
Management command to ensure demo content exists
This runs automatically on deployment to populate the database
"""
from django.core.management.base import BaseCommand
from content.models import CompanyInfo, Service, Statistic


class Command(BaseCommand):
    help = 'Ensures demo content exists in the database for owner review'

    def handle(self, *args, **options):
        self.stdout.write('Checking for demo content...')
        
        # Check if company info exists
        if not CompanyInfo.objects.exists():
            self.stdout.write('Creating demo company information...')
            self.create_company_info()
        else:
            self.stdout.write('✅ Company info already exists')
        
        # Check if services exist
        if Service.objects.count() < 3:
            self.stdout.write('Creating demo services...')
            self.create_services()
        else:
            self.stdout.write('✅ Services already exist')
        
        # Check if statistics exist
        if Statistic.objects.count() < 4:
            self.stdout.write('Creating demo statistics...')
            self.create_statistics()
        else:
            self.stdout.write('✅ Statistics already exist')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Demo content is ready!'))
        self.stdout.write('View in English: /en/')
        self.stdout.write('View in Tamil: /ta/')
        self.stdout.write('View in Hindi: /hi/')

    def create_company_info(self):
        """Create company information in all languages"""
        company = CompanyInfo()
        
        # English content
        company.company_name_en = "Propertism Realty Advisors LLP"
        company.tagline_en = "Your Trusted NRI Property Partner"
        company.hero_title_en = "NRI Property Management Services In Chennai, India"
        company.hero_description_en = "We manage your property and resources when you are far from the nation"
        company.hero_eyebrow_en = "Propertism Realty Advisors"
        company.about_mission_en = "To provide exceptional property management services for Non-Resident Indians, ensuring their investments are secure and well-maintained."
        company.about_description_en = "Propertism Realty Advisors LLP specializes in comprehensive property management services for NRI clients. With offices in Chennai, India and Hackensack, NJ, USA, we bridge the gap between overseas property owners and their investments in India."
        
        # Tamil content
        company.company_name_ta = "ப்ராபர்டிசம் ரியாலிட்டி அட்வைசர்ஸ் எல்எல்பி"
        company.tagline_ta = "உங்கள் நம்பகமான NRI சொத்து பங்குதாரர்"
        company.hero_title_ta = "சென்னை, இந்தியாவில் NRI சொத்து மேலாண்மை சேவைகள்"
        company.hero_description_ta = "நீங்கள் நாட்டிலிருந்து தொலைவில் இருக்கும்போது உங்கள் சொத்து மற்றும் வளங்களை நாங்கள் நிர்வகிக்கிறோம்"
        company.hero_eyebrow_ta = "ப்ராபர்டிசம் ரியாலிட்டி அட்வைசர்ஸ்"
        company.about_mission_ta = "வெளிநாட்டு இந்தியர்களுக்கு சிறந்த சொத்து மேலாண்மை சேவைகளை வழங்குதல், அவர்களின் முதலீடுகள் பாதுகாப்பாகவும் நன்கு பராமரிக்கப்படுவதையும் உறுதி செய்தல்."
        company.about_description_ta = "ப்ராபர்டிசம் ரியாலிட்டி அட்வைசர்ஸ் எல்எல்பி NRI வாடிக்கையாளர்களுக்கான விரிவான சொத்து மேலாண்மை சேவைகளில் நிபுணத்துவம் பெற்றுள்ளது. சென்னை, இந்தியா மற்றும் ஹேக்கன்சாக், NJ, USA இல் அலுவலகங்களுடன், வெளிநாட்டு சொத்து உரிமையாளர்கள் மற்றும் இந்தியாவில் அவர்களின் முதலீடுகளுக்கு இடையே பாலம் அமைக்கிறோம்."
        
        # Hindi content
        company.company_name_hi = "प्रॉपर्टिज्म रियल्टी एडवाइजर्स एलएलपी"
        company.tagline_hi = "आपका विश्वसनीय NRI संपत्ति साझेदार"
        company.hero_title_hi = "चेन्नई, भारत में NRI संपत्ति प्रबंधन सेवाएं"
        company.hero_description_hi = "जब आप देश से दूर हों तो हम आपकी संपत्ति और संसाधनों का प्रबंधन करते हैं"
        company.hero_eyebrow_hi = "प्रॉपर्टिज्म रियल्टी एडवाइजर्स"
        company.about_mission_hi = "अनिवासी भारतीयों के लिए असाधारण संपत्ति प्रबंधन सेवाएं प्रदान करना, यह सुनिश्चित करना कि उनके निवेश सुरक्षित और अच्छी तरह से बनाए रखे गए हैं।"
        company.about_description_hi = "प्रॉपर्टिज्म रियल्टी एडवाइजर्स एलएलपी NRI ग्राहकों के लिए व्यापक संपत्ति प्रबंधन सेवाओं में विशेषज्ञता रखता है। चेन्नई, भारत और हैकेनसैक, NJ, USA में कार्यालयों के साथ, हम विदेशी संपत्ति मालिकों और भारत में उनके निवेश के बीच की खाई को पाटते हैं।"
        
        # Contact information
        company.india_office_address = "Chennai, Tamil Nadu"
        company.india_office_city = "Chennai"
        company.india_office_state = "Tamil Nadu"
        company.india_office_pincode = "600093"
        company.india_phone_1 = "+91-86670-20798"
        
        company.us_office_address = "Hackensack, NJ"
        company.us_office_city = "Hackensack"
        company.us_office_state = "NJ"
        company.us_office_zipcode = "07601"
        company.us_phone = "+1-XXX-XXX-XXXX"
        
        company.email = "info@propertism.com"
        company.business_hours = "Monday - Saturday: 9:00 AM - 6:00 PM IST"
        
        company.save()
        self.stdout.write('✅ Company information created')

    def create_services(self):
        """Create services in all languages"""
        services_data = [
            {
                'title_en': 'Real Estate Buy & Sell',
                'title_ta': 'ரியல் எஸ்டேட் வாங்குதல் & விற்பனை',
                'title_hi': 'रियल एस्टेट खरीद और बिक्री',
                'short_description_en': 'Expert guidance for buying and selling properties in Chennai',
                'short_description_ta': 'சென்னையில் சொத்துக்களை வாங்குவதற்கும் விற்பதற்கும் நிபுணர் வழிகாட்டுதல்',
                'short_description_hi': 'चेन्नई में संपत्ति खरीदने और बेचने के लिए विशेषज्ञ मार्गदर्शन',
                'full_description_en': 'We provide comprehensive real estate services for NRI clients looking to buy or sell properties in Chennai. Our team handles everything from property search to legal documentation.',
                'full_description_ta': 'சென்னையில் சொத்துக்களை வாங்க அல்லது விற்க விரும்பும் NRI வாடிக்கையாளர்களுக்கு விரிவான ரியல் எஸ்டேட் சேவைகளை வழங்குகிறோம். சொத்து தேடல் முதல் சட்ட ஆவணங்கள் வரை எல்லாவற்றையும் எங்கள் குழு கையாளுகிறது.',
                'full_description_hi': 'हम चेन्नई में संपत्ति खरीदने या बेचने के इच्छुक NRI ग्राहकों के लिए व्यापक रियल एस्टेट सेवाएं प्रदान करते हैं। हमारी टीम संपत्ति खोज से लेकर कानूनी दस्तावेज़ीकरण तक सब कुछ संभालती है।',
                'icon': '🏢',
                'order': 1
            },
            {
                'title_en': 'Rental & Maintenance',
                'title_ta': 'வாடகை & பராமரிப்பு',
                'title_hi': 'किराया और रखरखाव',
                'short_description_en': 'Complete rental management and property maintenance services',
                'short_description_ta': 'முழுமையான வாடகை மேலாண்மை மற்றும் சொத்து பராமரிப்பு சேவைகள்',
                'short_description_hi': 'पूर्ण किराया प्रबंधन और संपत्ति रखरखाव सेवाएं',
                'full_description_en': 'Professional tenant management, rent collection, and property maintenance services. We ensure your property is well-maintained and generates steady rental income.',
                'full_description_ta': 'தொழில்முறை குத்தகைதாரர் மேலாண்மை, வாடகை வசூல் மற்றும் சொத்து பராமரிப்பு சேவைகள். உங்கள் சொத்து நன்கு பராமரிக்கப்படுவதையும் நிலையான வாடகை வருமானத்தை உருவாக்குவதையும் நாங்கள் உறுதி செய்கிறோம்.',
                'full_description_hi': 'पेशेवर किरायेदार प्रबंधन, किराया संग्रह और संपत्ति रखरखाव सेवाएं। हम सुनिश्चित करते हैं कि आपकी संपत्ति अच्छी तरह से बनाए रखी गई है और स्थिर किराये की आय उत्पन्न करती है।',
                'icon': '🔧',
                'order': 2
            },
            {
                'title_en': 'Industrial Land Services',
                'title_ta': 'தொழில்துறை நில சேவைகள்',
                'title_hi': 'औद्योगिक भूमि सेवाएं',
                'short_description_en': 'Specialized services for industrial land acquisition and development',
                'short_description_ta': 'தொழில்துறை நில கையகப்படுத்தல் மற்றும் மேம்பாட்டிற்கான சிறப்பு சேவைகள்',
                'short_description_hi': 'औद्योगिक भूमि अधिग्रहण और विकास के लिए विशेष सेवाएं',
                'full_description_en': 'Expert advisory for industrial land purchases, development approvals, and project management. We help businesses establish their presence in Chennai.',
                'full_description_ta': 'தொழில்துறை நில கொள்முதல், மேம்பாட்டு அனுமதிகள் மற்றும் திட்ட மேலாண்மைக்கான நிபுணர் ஆலோசனை. சென்னையில் தங்கள் இருப்பை நிறுவ வணிகங்களுக்கு நாங்கள் உதவுகிறோம்.',
                'full_description_hi': 'औद्योगिक भूमि खरीद, विकास अनुमोदन और परियोजना प्रबंधन के लिए विशेषज्ञ सलाह। हम व्यवसायों को चेन्नई में अपनी उपस्थिति स्थापित करने में मदद करते हैं।',
                'icon': '🏭',
                'order': 3
            }
        ]
        
        for service_data in services_data:
            Service.objects.get_or_create(
                order=service_data['order'],
                defaults={
                    'title_en': service_data['title_en'],
                    'title_ta': service_data['title_ta'],
                    'title_hi': service_data['title_hi'],
                    'short_description_en': service_data['short_description_en'],
                    'short_description_ta': service_data['short_description_ta'],
                    'short_description_hi': service_data['short_description_hi'],
                    'full_description_en': service_data['full_description_en'],
                    'full_description_ta': service_data['full_description_ta'],
                    'full_description_hi': service_data['full_description_hi'],
                    'icon': service_data['icon'],
                    'is_active': True
                }
            )
        
        self.stdout.write('✅ Services created')

    def create_statistics(self):
        """Create company statistics"""
        stats_data = [
            {'label': 'Properties Managed', 'value': '500+', 'order': 1},
            {'label': 'Happy NRI Clients', 'value': '200+', 'order': 2},
            {'label': 'Years of Experience', 'value': '10+', 'order': 3},
            {'label': 'Cities Covered', 'value': '5+', 'order': 4},
        ]
        
        for stat_data in stats_data:
            Statistic.objects.get_or_create(
                order=stat_data['order'],
                defaults={
                    'label': stat_data['label'],
                    'value': stat_data['value'],
                    'is_active': True
                }
            )
        
        self.stdout.write('✅ Statistics created')
