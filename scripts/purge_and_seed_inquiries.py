import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings")

import django
django.setup()

from properties.models import Inquiry, Property
from django.utils import timezone

# 1. Purge
print("Purging all existing inquiries...")
deleted_count, _ = Inquiry.objects.all().delete()
print(f"Deleted {deleted_count} inquiries.")

# Ensure properties exist for quick inquiries
print("\nEnsuring properties exist...")
properties_map = {}
for p_title, p_loc, p_type, p_price in [
    ("3BHK Apartment in Adyar", "Adyar, Chennai", "sale", 25000000),
    ("4BHK Villa in ECR", "ECR, Chennai", "sale", 55000000),
    ("2BHK Flat in Velachery", "Velachery, Chennai", "rent", 12000000)
]:
    p, created = Property.objects.get_or_create(
        title=p_title,
        defaults={
            "price": p_price,
            "description": f"Beautiful {p_title} in prime location.",
            "location": p_loc,
            "price_type": p_type
        }
    )
    properties_map[p_title] = p
    if created:
        print(f"Created property: {p_title}")
    else:
        print(f"Found existing property: {p_title}")

# 2. Seed fresh inquiries for each intent
inquiries_to_create = [
    {
        "name": "Arun Kumar (Seller)",
        "email": "arun.seller@example.com",
        "phone": "+919840123456",
        "form_source": "General Inquiry",
        "property_title": None,
        "service_needed": "buy-sell",
        "property_type": "apartment",
        "locality": "adyar",
        "user_role": "owner",
        "nri_status": "No",
        "message": (
            "I am looking to sell my 3 BHK apartment in Adyar. It is in excellent condition and ready for viewings.\n\n"
            "--- Additional Details ---\n"
            "Service Required: Sell\n"
            "Property Type: Apartment\n"
            "Locality/Area: Adyar, Chennai\n"
            "User Role: Property Owner\n"
            "NRI Status: No"
        )
    },
    {
        "name": "Meera Ramakrishnan (Landlord)",
        "email": "meera.landlord@example.com",
        "phone": "+919840987654",
        "form_source": "General Inquiry",
        "property_title": None,
        "service_needed": "rental",
        "property_type": "villa",
        "locality": "omr",
        "user_role": "owner",
        "nri_status": "Yes",
        "message": (
            "I want to rent out my independent villa in OMR. Looking for corporate tenants.\n\n"
            "--- Additional Details ---\n"
            "Service Required: Rent\n"
            "Property Type: Villa\n"
            "Locality/Area: Sholinganallur (OMR), Chennai\n"
            "User Role: Property Owner\n"
            "NRI Status: Yes"
        )
    },
    {
        "name": "Rajesh Nair (NRI Owner)",
        "email": "rajesh.nri@example.com",
        "phone": "+14085551234",
        "form_source": "General Inquiry",
        "property_title": None,
        "service_needed": "industrial",
        "property_type": "commercial",
        "locality": "t-nagar",
        "user_role": "owner",
        "nri_status": "Yes",
        "message": (
            "I reside in the US and need full property management services for my commercial space in T. Nagar.\n\n"
            "--- Additional Details ---\n"
            "Service Required: Manage\n"
            "Property Type: Commercial\n"
            "Locality/Area: T. Nagar, Chennai\n"
            "User Role: Property Owner\n"
            "NRI Status: Yes"
        )
    },
    # 3 Quick Inquiry entries
    {
        "name": "Kavitha Sundaram",
        "email": "kavitha.sundaram@gmail.com",
        "phone": "9876543210",
        "form_source": "Quick Inquiry",
        "property_title": "3BHK Apartment in Adyar",
        "service_needed": "buy-sell",
        "property_type": "apartment",
        "locality": "Adyar, Chennai",
        "user_role": "buyer",
        "nri_status": "No",
        "message": (
            "Interested in buying this property. Please share pricing details and available floor plans.\n\n"
            "--- Additional Details ---\n"
            "User Role: Buyer / Tenant\n"
            "NRI Status: No\n"
            "Preferred Contact Mode: Direct Phone Call\n\n"
            "--- Traffic Attribution Parameters ---\n"
            "Referrer: https://www.google.com/\n"
            "Landing Page: https://www.propertism.in/properties/3bhk-apartment-adyar/"
        )
    },
    {
        "name": "Anand Raghavan",
        "email": "anand.raghavan@outlook.com",
        "phone": "+14085559876",
        "form_source": "Quick Inquiry",
        "property_title": "4BHK Villa in ECR",
        "service_needed": "industrial",
        "property_type": "villa",
        "locality": "ECR, Chennai",
        "user_role": "owner",
        "nri_status": "Yes",
        "message": (
            "I am an NRI based in San Francisco. Looking for property management services for this villa. Currently unoccupied and need tenant placement + maintenance.\n\n"
            "--- Additional Details ---\n"
            "User Role: Property Owner\n"
            "NRI Status: Yes\n"
            "Preferred Contact Mode: WhatsApp Message\n\n"
            "--- Traffic Attribution Parameters ---\n"
            "Referrer: https://www.google.com/\n"
            "Landing Page: https://www.propertism.in/properties/4bhk-villa-ecr/"
        )
    },
    {
        "name": "Deepika Mohan",
        "email": "deepika.m@yahoo.co.in",
        "phone": "8901234567",
        "form_source": "Quick Inquiry",
        "property_title": "2BHK Flat in Velachery",
        "service_needed": "rental",
        "property_type": "apartment",
        "locality": "Velachery, Chennai",
        "user_role": "buyer",
        "nri_status": "No",
        "message": (
            "Looking to rent this flat for my family. We can move in by August. Please share rental terms and schedule a visit.\n\n"
            "--- Additional Details ---\n"
            "User Role: Buyer / Tenant\n"
            "NRI Status: No\n"
            "Preferred Contact Mode: WhatsApp Message\n\n"
            "--- Traffic Attribution Parameters ---\n"
            "Referrer: android-app://com.google.android.googlequicksearchbox/\n"
            "Landing Page: https://www.propertism.in/properties/2bhk-flat-velachery/"
        )
    }
]

print("\nSeeding fresh inquiries...")
for data in inquiries_to_create:
    prop_instance = None
    if data["property_title"]:
        prop_instance = properties_map.get(data["property_title"])
        
    inq = Inquiry.objects.create(
        property=prop_instance,
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        message=data["message"],
        status="pending",
        form_source=data["form_source"],
        service_needed=data.get("service_needed"),
        property_type=data.get("property_type"),
        locality=data.get("locality"),
        user_role=data.get("user_role"),
        nri_status=data.get("nri_status"),
        confidence_score=95,
        assessment_status="Genuine",
        validation_summary="Simulated organic lead"
    )
    # Lock original timestamp
    Inquiry.objects.filter(pk=inq.pk).update(
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    print(f"Created Inquiry ID: {inq.id} - {inq.name} ({data['email']}) [Source: {data['form_source']}]")

print("\nDone! Seeding completed successfully.")
