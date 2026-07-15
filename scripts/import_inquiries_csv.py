import csv
import os
import sys
from datetime import datetime

# Setup Django path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings")

import django
django.setup()

from properties.models import Inquiry, Property
from django.utils.timezone import make_aware

# Path to the CSV
csv_path = r"D:\viji\viji-olivine\03rolledout\06propertism.deal.engine\inquiries_20260714_1326.csv"

# 1. Delete existing inquiries
print("Deleting existing test data from Inquiry model...")
deleted_count, _ = Inquiry.objects.all().delete()
print(f"Deleted {deleted_count} inquiries.")

# 2. Import CSV data
print(f"Reading CSV from {csv_path}...")
imported_count = 0

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row_id = int(row['ID'])
        name = row['Name'].strip()
        email = row['Email'].strip()
        phone = row['Phone'].strip()
        message = row['Message'].strip()
        status_val = row['Status'].strip().lower()
        property_val = row['Property'].strip()
        submitted_str = row['Submitted'].strip()
        
        # Parse submitted datetime
        naive_dt = datetime.strptime(submitted_str, "%Y-%m-%d %H:%M")
        submitted_dt = make_aware(naive_dt)
        
        # Lookup property if not General
        prop_instance = None
        if property_val and property_val != 'General':
            prop_instance = Property.objects.filter(title__iexact=property_val).first()
            if not prop_instance:
                # Try icontains
                prop_instance = Property.objects.filter(title__icontains=property_val).first()
            if not prop_instance:
                print(f"[WARNING] Property '{property_val}' not found in database. Setting property to None.")
        
        # Create Inquiry instance
        inquiry = Inquiry.objects.create(
            id=row_id,
            name=name,
            email=email,
            phone=phone,
            message=message,
            status=status_val,
            property=prop_instance,
        )
        
        # Update timestamps to bypass auto_now / auto_now_add override
        Inquiry.objects.filter(id=inquiry.id).update(
            created_at=submitted_dt,
            updated_at=submitted_dt
        )
        print(f"Imported row ID {row_id} for {name}")
        imported_count += 1

print(f"Successfully imported {imported_count} inquiries from CSV.")
