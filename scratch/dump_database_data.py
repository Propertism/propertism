import os
import sys
import json
from collections import Counter

# Set up Django environment
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realtor_project.settings")
import django
django.setup()

from properties.models import Inquiry, ContactMessage
from chat.models import RealBotSession, RealBotMessage
from nri_assist.models import NRIAssistEvent, NRIService

def dump_data():
    out_file = os.path.join(PROJECT_ROOT, "scratch", "db_dump_output.txt")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("--- INQUIRIES ---\n")
        inquiries = Inquiry.objects.all().order_by('created_at')
        f.write(f"Total Inquiries: {inquiries.count()}\n")
        for idx, i in enumerate(inquiries, 1):
            f.write(f"\n{idx}. Inquiry ID: {i.id}\n")
            f.write(f"   Name: {i.name}\n")
            f.write(f"   Email: {i.email}\n")
            f.write(f"   Phone: {i.phone}\n")
            f.write(f"   Source: {i.form_source}\n")
            f.write(f"   Status: {i.status}\n")
            f.write(f"   Confidence Score: {i.confidence_score}\n")
            f.write(f"   Spam Score: {i.spam_score}\n")
            f.write(f"   Assessment Status: {i.assessment_status}\n")
            f.write(f"   Validation Summary: {json.dumps(i.validation_summary)}\n")
            f.write(f"   Message: {i.message}\n")
            f.write(f"   Created At: {i.created_at}\n")

        f.write("\n--- CONTACT MESSAGES ---\n")
        messages = ContactMessage.objects.all().order_by('created_at')
        f.write(f"Total Contact Messages: {messages.count()}\n")
        for idx, m in enumerate(messages, 1):
            f.write(f"\n{idx}. Message ID: {m.id}\n")
            f.write(f"   Name: {m.name}\n")
            f.write(f"   Email: {m.email}\n")
            f.write(f"   Phone: {m.phone}\n")
            f.write(f"   Subject: {m.subject}\n")
            f.write(f"   Status: {m.status}\n")
            f.write(f"   Message: {m.message}\n")
            f.write(f"   Created At: {m.created_at}\n")

        f.write("\n--- REALBOT SESSIONS ---\n")
        sessions = RealBotSession.objects.all()
        f.write(f"Total Sessions: {sessions.count()}\n")
        for idx, s in enumerate(sessions, 1):
            f.write(f"\nSession {idx}: ID: {s.session_id} | Created: {s.created_at} | Updated: {s.updated_at}\n")
            msgs = RealBotMessage.objects.filter(session=s).order_by('created_at')
            f.write(f"   Messages count: {msgs.count()}\n")
            for m in msgs:
                f.write(f"     [{m.sender}]: {m.text}\n")

        f.write("\n--- NRI ASSIST EVENTS ---\n")
        events = NRIAssistEvent.objects.all()
        f.write(f"Total Events: {events.count()}\n")
        event_types = Counter(e.event_type for e in events)
        f.write(f"Event Types Breakdown: {dict(event_types)}\n")
        
        for idx, e in enumerate(events, 1):
            f.write(f"\n{idx}. Event: {e.event_type} | Category: {e.service_category} | IP: {e.ip_address} | Metadata: {json.dumps(e.metadata)} | Time: {e.created_at}\n")

    print(f"Data successfully dumped to {out_file}")

if __name__ == "__main__":
    dump_data()
