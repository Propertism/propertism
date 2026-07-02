from django.conf import settings
from .site_context import get_active_services, get_company_info, get_home_section_links


def site_content(request):
    company = get_company_info()
    footer_services = get_active_services(limit=4)
    return {
        "company": company,
        "footer_services": footer_services,
        "home_section_links": get_home_section_links(),
        "clarity_project_id": getattr(settings, "CLARITY_PROJECT_ID", ""),
        "chat_widget_content": {
            "title": company.chat_window_title or "Leave a message",
            "subtitle": company.chat_window_subtitle or "We'll get back to you soon",
            "submitText": company.chat_submit_text or "Send",
            "sendingText": company.chat_sending_text or "Sending...",
            "successTitle": company.chat_success_title or "Message sent!",
            "successMessage": company.chat_success_message or "Thanks for reaching out. We'll get back to you within 24 hours.",
        },
    }
