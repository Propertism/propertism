"""
chat/response_config.py — Predefined response components for realBOT M2.9.
Defines template strings, rendering priority weights, and expected content keys schema
for each of the 21 standard components.
"""

DEFAULT_COMPONENTS = [
    # ── 1. Content/Card Components ────────────────────────────────────────────
    {
        'name': 'plain_text',
        'component_type': 'text',
        'display_template': '{text}',
        'content_model': {'text': 'Hello, how can I help you?'},
        'data_schema': ['text'],
        'rendering_priority': 5,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'service_card',
        'component_type': 'card',
        'display_template': '### Service: {service_name}\n\n{description}\n\n* **Pricing:** {pricing}\n* **Benefits:** {benefits}',
        'content_model': {
            'service_name': 'Property Management',
            'description': 'End-to-end management for NRIs.',
            'pricing': '10% of monthly rent',
            'benefits': 'Rent collection, tenant sourcing, regular maintenance.'
        },
        'data_schema': ['service_name', 'description', 'pricing', 'benefits'],
        'rendering_priority': 10,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'knowledge_card',
        'component_type': 'card',
        'display_template': '### FAQ: {title}\n\n{content}\n\n[Read complete article]({url})',
        'content_model': {
            'title': 'How to get Patta?',
            'content': 'Apply online via TN eservices portal.',
            'url': '/faq/'
        },
        'data_schema': ['title', 'content', 'url'],
        'rendering_priority': 15,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'contact_card',
        'component_type': 'card',
        'display_template': '### Contact Us\n\n* **Phone:** {phone}\n* **Email:** {email}\n* **Address:** {address}',
        'content_model': {
            'phone': '+91 86670 20798',
            'email': 'info@propertism.in',
            'address': 'Saligramam, Chennai - 600093'
        },
        'data_schema': ['phone', 'email', 'address'],
        'rendering_priority': 25,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'property_card',
        'component_type': 'card',
        'display_template': '### Property: {title}\n\n* **Type:** {property_type}\n* **Price:** {price}\n* **Location:** {locality}, Chennai\n\n[View Details]({details_url})',
        'content_model': {
            'title': 'Premium 3BHK Villa',
            'property_type': 'Villa',
            'price': '₹1.5 Crores',
            'locality': 'ECR',
            'details_url': '/properties/1/'
        },
        'data_schema': ['title', 'property_type', 'price', 'locality', 'details_url'],
        'rendering_priority': 12,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'navigation_card',
        'component_type': 'card',
        'display_template': '### Go to {label}\n\n[Click here to visit]({url})',
        'content_model': {
            'label': 'Resource Hub',
            'url': '/property-owner-resources/'
        },
        'data_schema': ['label', 'url'],
        'rendering_priority': 20,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'government_service_card',
        'component_type': 'card',
        'display_template': '### Government Portal: {service_name}\n\nAccess the official link for {description}:\n\n[Launch Portal]({url})',
        'content_model': {
            'service_name': 'Patta/Chitta Extract',
            'description': 'Tamil Nadu Land Records',
            'url': 'https://eservices.tn.gov.in/'
        },
        'data_schema': ['service_name', 'description', 'url'],
        'rendering_priority': 30,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'office_location_card',
        'component_type': 'card',
        'display_template': '### Chennai Main Office\n\n* **Address:** {address}\n\n[Open in Google Maps]({maps_url})',
        'content_model': {
            'address': 'No. 30, 3rd Floor, Pankajam Towers, Saligramam, Chennai - 600093',
            'maps_url': 'https://maps.google.com/?q=Propertism+Realty+Advisors+Chennai'
        },
        'data_schema': ['address', 'maps_url'],
        'rendering_priority': 28,
        'status': 'active',
        'version': 1,
    },

    # ── 2. Communication Component Cards ──────────────────────────────────────
    {
        'name': 'whatsapp_card',
        'component_type': 'card',
        'display_template': '### Connect on WhatsApp\n\nChat directly with our NRI support advisor:\n\n[Launch WhatsApp]({wa_url})',
        'content_model': {
            'wa_url': 'https://wa.me/918667020798'
        },
        'data_schema': ['wa_url'],
        'rendering_priority': 24,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'phone_call_card',
        'component_type': 'card',
        'display_template': '### Call Client Desk\n\n* **Phone:** {phone}',
        'content_model': {
            'phone': '+91 86670 20798'
        },
        'data_schema': ['phone'],
        'rendering_priority': 22,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'email_card',
        'component_type': 'card',
        'display_template': '### Send Email Enquiry\n\n* **Email:** {email}',
        'content_model': {
            'email': 'info@propertism.in'
        },
        'data_schema': ['email'],
        'rendering_priority': 26,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'linkedin_card',
        'component_type': 'card',
        'display_template': '### Follow Us on LinkedIn\n\n[Visit LinkedIn Profile]({url})',
        'content_model': {
            'url': 'https://www.linkedin.com/company/propertism'
        },
        'data_schema': ['url'],
        'rendering_priority': 27,
        'status': 'active',
        'version': 1,
    },

    # ── 3. Inquiry & Action Workflow Cards ───────────────────────────────────
    {
        'name': 'inquiry_summary_card',
        'component_type': 'card',
        'display_template': '### Inquiry Details Captured\n\n* **Name:** {name}\n* **Mobile:** {phone}\n* **Email:** {email}\n* **Service:** {service}\n* **Message:** {message}',
        'content_model': {
            'name': 'Vijay',
            'phone': '+91 86670 20798',
            'email': 'info@propertism.in',
            'service': 'Buy Property',
            'message': 'Looking for a villa in Chennai'
        },
        'data_schema': ['name', 'phone', 'email', 'service', 'message'],
        'rendering_priority': 8,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'inquiry_confirmation_card',
        'component_type': 'card',
        'display_template': '### Submit Your Inquiry?\n\nPlease review your details above. Select **Confirm** to submit or **Cancel** to abort.',
        'content_model': {},
        'data_schema': [],
        'rendering_priority': 9,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'action_confirmation_card',
        'component_type': 'card',
        'display_template': '### Confirm Action\n\n{prompt_text}\n\n[Yes, Proceed]({proceed_url}) | [Cancel]({cancel_url})',
        'content_model': {
            'prompt_text': 'Are you sure you want to navigate away?',
            'proceed_url': '#',
            'cancel_url': '#'
        },
        'data_schema': ['prompt_text', 'proceed_url', 'cancel_url'],
        'rendering_priority': 7,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'suggestion_chips',
        'component_type': 'chips',
        'display_template': '{chips}',
        'content_model': {
            'chips': ['Buy Property', 'Sell Property', 'Contact Advisor']
        },
        'data_schema': ['chips'],
        'rendering_priority': 50,  # Chips always display at the very bottom
        'status': 'active',
        'version': 1,
    },

    # ── 4. System Card Components ─────────────────────────────────────────────
    {
        'name': 'warning_card',
        'component_type': 'alert',
        'display_template': '⚠️ **Warning:** {warning_message}',
        'content_model': {
            'warning_message': 'Please verify all inputs before submission.'
        },
        'data_schema': ['warning_message'],
        'rendering_priority': 3,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'information_card',
        'component_type': 'alert',
        'display_template': 'ℹ️ **Info:** {info_message}',
        'content_model': {
            'info_message': 'Your session expires in 30 minutes.'
        },
        'data_schema': ['info_message'],
        'rendering_priority': 4,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'success_card',
        'component_type': 'alert',
        'display_template': '✅ **Success:** {success_message}',
        'content_model': {
            'success_message': 'Inquiry submitted successfully!'
        },
        'data_schema': ['success_message'],
        'rendering_priority': 2,
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'error_card',
        'component_type': 'alert',
        'display_template': '❌ **Error:** {error_message}',
        'content_model': {
            'error_message': 'Validation failed. Please correct input fields.'
        },
        'data_schema': ['error_message'],
        'rendering_priority': 1,  # Errors show at the very top
        'status': 'active',
        'version': 1,
    },
    {
        'name': 'empty_state_card',
        'component_type': 'card',
        'display_template': '### No Results Found\n\n{message}',
        'content_model': {
            'message': 'No properties match your current filters.'
        },
        'data_schema': ['message'],
        'rendering_priority': 6,
        'status': 'active',
        'version': 1,
    },
]
