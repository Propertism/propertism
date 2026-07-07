"""
chat/inquiry_validator.py — M2.6 Stateless Field Validators

Each validator returns (passed: bool, error_message: str).
All validators are independently testable and reusable across
chatbot, website forms, mobile apps, and future APIs.

Country-aware phone validation follows E.164 strict rules for
India, USA/Canada, UK, UAE, Singapore, Australia.
All other countries use lenient international format check.
"""
import re
import logging

from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

# ── Spam URL patterns (mirrors content.views.is_spam_inquiry) ─────────────────
_SPAM_URL_PATTERNS = re.compile(r'https?://|www\.\S+', re.IGNORECASE)

# ── Country-to-phone-spec map ─────────────────────────────────────────────────
# (prefix, digit_count_after_prefix_or_None_for_range, min_digits, max_digits)
COUNTRY_PHONE_SPECS = {
    'india':     ('+91',  10, 10),
    'usa':       ('+1',   10, 10),
    'canada':    ('+1',   10, 10),
    'uk':        ('+44',  None, 9, 10),
    'uae':       ('+971', None, 7, 9),
    'singapore': ('+65',  8,  8),
    'australia': ('+61',  None, 8, 9),
    'qatar':     ('+974', None, 7, 8),
    'bahrain':   ('+973', None, 7, 8),
    'kuwait':    ('+965', None, 7, 8),
    'oman':      ('+968', None, 7, 8),
    'saudi arabia': ('+966', None, 8, 9),
}

# Normalised country name → spec key
COUNTRY_SPEC_ALIAS = {
    'usa':             'usa',
    'united states':   'usa',
    'america':         'usa',
    'uk':              'uk',
    'united kingdom':  'uk',
    'england':         'uk',
    'britain':         'uk',
    'uae':             'uae',
    'united arab emirates': 'uae',
    'dubai':           'uae',
    'abu dhabi':       'uae',
    'india':           'india',
    'indian':          'india',
    'canada':          'canada',
    'canadian':        'canada',
    'australia':       'australia',
    'aus':             'australia',
    'australian':      'australia',
    'singapore':       'singapore',
    'sg':              'singapore',
    'qatar':           'qatar',
    'bahrain':         'bahrain',
    'kuwait':          'kuwait',
    'oman':            'oman',
    'saudi arabia':    'saudi arabia',
    'ksa':             'saudi arabia',
}

# Known budget chip values accepted verbatim
KNOWN_BUDGET_CHIPS = frozenset([
    'under ₹50l', '₹50l–₹1cr', '₹1cr–₹2cr', 'above ₹2cr',
])


class InquiryFieldValidator:
    """
    Stateless, deterministic field validator.
    Call via: InquiryFieldValidator().validate(field_name, value, context)
    context may contain: {'country': 'India'} for phone validation.
    """

    def validate(self, field_name: str, value: str, context: dict = None) -> tuple:
        """Route to the correct validator by field_name."""
        context = context or {}
        method = getattr(self, f'validate_{field_name}', None)
        if method is None:
            # Fall back to free_text for unregistered fields
            return self.validate_free_text(value)
        if field_name == 'phone' or field_name == 'mobile_number':
            country = context.get('country', '')
            return self.validate_phone(value, country)
        return method(value)

    # ── Individual validators ──────────────────────────────────────────────────

    def validate_customer_name(self, value: str) -> tuple:
        value = value.strip()
        if not value:
            return False, "I didn't catch your name. Could you please share it?"
        if len(value) < 2:
            return False, "Your name seems too short. Could you share your full name?"
        if len(value) > 100:
            return False, "That name is too long. Could you share a shorter version?"
        if not re.match(r"^[A-Za-z\s\-\'\.]+$", value):
            return False, "Your name seems to contain unexpected characters. Letters, spaces, hyphens, and apostrophes are accepted."
        return True, ''

    def validate_name(self, value: str) -> tuple:
        return self.validate_customer_name(value)

    def validate_phone(self, value: str, country: str = '') -> tuple:
        """
        Country-aware E.164 phone validation.
        Strict for known countries; lenient (international prefix + digits) for others.
        """
        value = value.strip()
        if not value:
            return False, "Please share your mobile number with country code."

        # Strip all spaces, hyphens, and parentheses for digit analysis
        cleaned = re.sub(r'[\s\-\(\)\.]+', '', value)

        # Must start with +
        if not cleaned.startswith('+'):
            return False, (
                "Please include the country code with your number "
                "(e.g. +91 9876543210 for India, +1 4085551234 for USA)."
            )

        # Extract digits after the + prefix
        digits_only = re.sub(r'[^\d]', '', cleaned[1:])

        if len(digits_only) < 7:
            return False, "That number seems too short. Please include the full number with country code."

        # Country-specific strict validation
        country_key = COUNTRY_SPEC_ALIAS.get(country.lower().strip())
        if country_key:
            spec = COUNTRY_PHONE_SPECS.get(country_key)
            if spec:
                if len(spec) == 3:
                    # (prefix, exact_count, exact_count)
                    prefix, exact, _ = spec
                    prefix_digits = re.sub(r'[^\d]', '', prefix)
                    subscriber_digits = digits_only[len(prefix_digits):]
                    if not digits_only.startswith(prefix_digits):
                        return False, (
                            f"For {country}, the number should start with {prefix} "
                            f"followed by {exact} digits. Please check and re-enter."
                        )
                    if len(subscriber_digits) != exact:
                        return False, (
                            f"For {country}, the number should have exactly {exact} digits "
                            f"after the country code. You provided {len(subscriber_digits)}."
                        )
                elif len(spec) == 4:
                    # (prefix, None, min_digits, max_digits)
                    prefix, _, min_d, max_d = spec
                    prefix_digits = re.sub(r'[^\d]', '', prefix)
                    subscriber_digits = digits_only[len(prefix_digits):]
                    if not digits_only.startswith(prefix_digits):
                        return False, (
                            f"For {country}, the number should start with {prefix}. "
                            "Please check and re-enter."
                        )
                    if not (min_d <= len(subscriber_digits) <= max_d):
                        return False, (
                            f"For {country}, the number should have {min_d}–{max_d} digits "
                            f"after the country code. You provided {len(subscriber_digits)}."
                        )
                return True, ''

        # Lenient fallback: international prefix present + total digits 7–15
        if 7 <= len(digits_only) <= 15:
            return True, ''

        return False, (
            "That doesn't look like a valid international phone number. "
            "Please include the country code (e.g. +65 91234567)."
        )

    def validate_mobile_number(self, value: str) -> tuple:
        # Called without context — use base phone logic (lenient)
        return self.validate_phone(value)

    def validate_email(self, value: str) -> tuple:
        value = value.strip()
        if not value:
            return False, "That email address appears to be empty."
        try:
            django_validate_email(value)
            return True, ''
        except ValidationError:
            return False, (
                "That doesn't look like a valid email address. "
                "Please use the format: name@example.com"
            )

    def validate_email_address(self, value: str) -> tuple:
        return self.validate_email(value)

    def validate_country(self, value: str) -> tuple:
        value = value.strip()
        if not value:
            return False, "Could you please tell me which country you are based in?"
        if len(value) < 2:
            return False, "That country name seems too short. Could you be more specific?"
        return True, ''

    def validate_service(self, value: str) -> tuple:
        value = value.strip()
        if not value:
            return False, "Please let me know what service you are looking for."
        if len(value) < 2:
            return False, "Could you share a bit more about the service you need?"
        return True, ''

    def validate_service_required(self, value: str) -> tuple:
        return self.validate_service(value)

    def validate_message(self, value: str) -> tuple:
        value = value.strip()
        if not value:
            return False, "Could you describe your requirement in a few words?"
        if len(value) < 5:
            return False, "Could you add a bit more detail to help our team understand your requirement?"
        if _SPAM_URL_PATTERNS.search(value):
            return False, "Please describe your requirement without URLs."
        return True, ''

    def validate_inquiry_message(self, value: str) -> tuple:
        return self.validate_message(value)

    def validate_budget(self, value: str) -> tuple:
        value = value.strip()
        if not value:
            return True, ''  # Optional — empty is fine
        if value.lower() in KNOWN_BUDGET_CHIPS:
            return True, ''
        # Accept any budget description: ₹ amounts, "50 lakh", "2 crore", "USD 100k", etc.
        if len(value) >= 1:
            return True, ''
        return False, "Could you share your approximate budget?"

    def validate_free_text(self, value: str) -> tuple:
        """Accept any non-empty string for open-ended optional fields."""
        value = value.strip()
        if not value:
            return True, ''  # Empty is acceptable for optional fields
        return True, ''
