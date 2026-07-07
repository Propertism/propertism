"""
chat/inquiry_extractor.py — M2.6 Deterministic Field Extractor (Annexure A Core)

Processes every customer message and extracts all detectable field values in a
single pass using keyword dictionaries, regular expressions, and phrase patterns.

NO artificial intelligence. NO probabilistic inference.
Every extraction rule is fully deterministic and independently testable.

Returns FieldExtractionResult containing:
  extracted   — raw matched strings per field
  validated   — clean validated values ready to store in collected_data
  conflicts   — fields where a new value differs from an already-collected value
  invalid     — fields where a value was found but failed validation
  fields_enriched — count of net-new fields added to this session
"""
import re
import logging
from dataclasses import dataclass, field

from chat.inquiry_fields import (
    KNOWN_COUNTRIES,
    SERVICE_KEYWORD_MAP,
    PROPERTY_TYPE_KEYWORDS,
    CHENNAI_LOCATION_KEYWORDS,
    TIMELINE_KEYWORDS,
    CONTACT_TIME_KEYWORDS,
)
from chat.inquiry_validator import InquiryFieldValidator

logger = logging.getLogger(__name__)

# ── Compiled regex patterns ───────────────────────────────────────────────────

# E-mail (simplified RFC 5322)
_RE_EMAIL = re.compile(r'\b[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}\b', re.IGNORECASE)

# International phone: +prefix digits (allows spaces/hyphens between groups)
_RE_PHONE = re.compile(
    r'\+\d{1,4}[\s\-\.]?\(?\d{1,5}\)?[\s\-\.]?\d{3,5}[\s\-\.]?\d{3,5}(?:[\s\-\.]\d{2,4})?',
    re.IGNORECASE,
)

# Budget patterns
_RE_BUDGET_INR = re.compile(
    r'₹\s?\d+(?:\.\d+)?\s?(?:lakh|lakhs|L|cr|crore|crores|Cr|k|K)?'
    r'|\d+(?:\.\d+)?\s?(?:lakh|lakhs|crore|crores)\s?(?:rupees?)?',
    re.IGNORECASE,
)
_RE_BUDGET_USD = re.compile(
    r'USD\s?\d+(?:\.\d+)?(?:\s?[kKmM])?|\$\s?\d+(?:\.\d+)?(?:\s?[kKmM])?',
    re.IGNORECASE,
)

# Name extraction patterns — captures name after common introductory phrases
_RE_NAME_PATTERNS = [
    re.compile(r'\bmy\s+name\s+is\s+([A-Za-z][A-Za-z\s\-\'\.]{1,50}?)(?:\.|,|$|\s+and\s|\s+from\s|\s+i\s)', re.IGNORECASE),
    re.compile(r'\bi\'?m\s+([A-Z][A-Za-z\s\-\'\.]{1,30}?)(?:\.|,|\s+from\s|\s+and\s|\s+based\s|$)', re.IGNORECASE),
    re.compile(r'\biam\s+([A-Z][A-Za-z\s\-\'\.]{1,30}?)(?:\.|,|\s+from\s|\s+and\s|$)', re.IGNORECASE),
    re.compile(r'^([A-Z][A-Za-z]{1,25}(?:\s+[A-Z][A-Za-z]{1,25}){1,3})\s+(?:here|speaking)', re.IGNORECASE),
    re.compile(r'\bname\s*[:–\-]\s*([A-Za-z][A-Za-z\s\-\'\.]{1,50}?)(?:\.|,|$)', re.IGNORECASE),
    re.compile(r'\bcall\s+me\s+([A-Za-z][A-Za-z\s\-\'\.]{1,30}?)(?:\.|,|$)', re.IGNORECASE),
    re.compile(r'\bthis\s+is\s+([A-Z][A-Za-z\s\-\'\.]{1,30}?)(?:\.|,|\s+from\s|\s+and\s|$)', re.IGNORECASE),
]

# ── Data class ────────────────────────────────────────────────────────────────

@dataclass
class FieldExtractionResult:
    extracted:       dict = field(default_factory=dict)   # field → raw match
    validated:       dict = field(default_factory=dict)   # field → clean value
    conflicts:       dict = field(default_factory=dict)   # field → new conflicting value
    invalid:         dict = field(default_factory=dict)   # field → error message
    fields_enriched: int  = 0                             # net-new fields accepted


# ── Main extractor ────────────────────────────────────────────────────────────

class InquiryFieldExtractor:
    """
    Deterministic multi-field extraction engine (Annexure A §3).

    Call extract(message, ics_session) for every customer message.
    The extractor:
      1. Runs all field-specific extractors against the message.
      2. Validates each extracted value via InquiryFieldValidator.
      3. Compares against existing collected_data for conflict detection.
      4. Returns FieldExtractionResult — caller decides what to persist.
    """

    def __init__(self):
        self._validator = InquiryFieldValidator()

    def extract(self, message: str, ics_session) -> FieldExtractionResult:
        """
        Main entry point. Runs all extractors in a single pass.
        ics_session.collected_data is read for conflict detection.
        Nothing is written here — caller persists via engine.
        """
        result = FieldExtractionResult()
        existing = ics_session.collected_data or {}
        context = {
            'country': existing.get('country', ''),
        }

        msg_lower = message.lower()

        # Run all extractors
        extractors = [
            ('customer_name',         self._extract_name),
            ('country',               self._extract_country),
            ('mobile_number',         self._extract_phone),
            ('email_address',         self._extract_email),
            ('service_required',      self._extract_service),
            ('property_type',         self._extract_property_type),
            ('preferred_location',    self._extract_location),
            ('budget',                self._extract_budget),
            ('timeline',              self._extract_timeline),
            ('preferred_contact_time', self._extract_contact_time),
        ]

        for field_name, extractor_fn in extractors:
            try:
                raw_value = extractor_fn(message, msg_lower)
            except Exception as exc:
                logger.warning(f'[InquiryFieldExtractor] Extractor error for {field_name}: {exc}')
                raw_value = None

            if raw_value is None:
                continue

            result.extracted[field_name] = raw_value

            # Validate
            if field_name == 'mobile_number':
                passed, error_msg = self._validator.validate_phone(raw_value, context.get('country', ''))
            else:
                validator_method = getattr(self._validator, f'validate_{field_name}', self._validator.validate_free_text)
                passed, error_msg = validator_method(raw_value)

            if not passed:
                result.invalid[field_name] = error_msg
                continue

            # Determine clean value
            clean_value = raw_value.strip()

            # Conflict detection (Annexure A §7)
            existing_value = existing.get(field_name)
            if existing_value and existing_value.lower() != clean_value.lower():
                result.conflicts[field_name] = clean_value
            elif not existing_value:
                result.validated[field_name] = clean_value
                result.fields_enriched += 1

        return result

    # ── Individual extractors ──────────────────────────────────────────────────

    def _extract_name(self, message: str, msg_lower: str):
        """Extract customer name from introductory phrases."""
        for pattern in _RE_NAME_PATTERNS:
            m = pattern.search(message)
            if m:
                candidate = m.group(1).strip().rstrip('.,')
                # Basic sanity: must be 2–80 chars, contain only letters/spaces/hyphens
                if 2 <= len(candidate) <= 80 and re.match(r"^[A-Za-z\s\-\'\.]+$", candidate):
                    return candidate
        return None

    def _extract_country(self, message: str, msg_lower: str):
        """Extract country from keyword dictionary (longest match first)."""
        # Sort by length descending to prefer longer phrases ("united states" over "states")
        for keyword in sorted(KNOWN_COUNTRIES.keys(), key=len, reverse=True):
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, msg_lower):
                return KNOWN_COUNTRIES[keyword]

        # Fallback: "from {Country}" or "based in {Country}" — two-word sequence
        m = re.search(
            r'\bfrom\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
            r'|\bbased\s+in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
            r'|\bi\s+am\s+in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b',
            message,
        )
        if m:
            candidate = (m.group(1) or m.group(2) or m.group(3) or '').strip()
            if candidate and len(candidate) >= 2:
                return candidate

        return None

    def _extract_phone(self, message: str, msg_lower: str):
        """Extract the first E.164-style phone number found in the message."""
        m = _RE_PHONE.search(message)
        if m:
            raw = m.group(0).strip()
            # Minimum sanity: must have + and at least 7 digits
            digits = re.sub(r'[^\d]', '', raw)
            if raw.startswith('+') and len(digits) >= 7:
                return raw
        return None

    def _extract_email(self, message: str, msg_lower: str):
        """Extract the first email address found."""
        m = _RE_EMAIL.search(message)
        return m.group(0).strip() if m else None

    def _extract_service(self, message: str, msg_lower: str):
        """
        Map message keywords to known service names.
        Longer phrases matched first to avoid "sell" matching inside "resell".
        """
        for keyword in sorted(SERVICE_KEYWORD_MAP.keys(), key=len, reverse=True):
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, msg_lower):
                return SERVICE_KEYWORD_MAP[keyword]
        return None

    def _extract_property_type(self, message: str, msg_lower: str):
        """Extract property type from keyword dictionary."""
        for keyword in sorted(PROPERTY_TYPE_KEYWORDS.keys(), key=len, reverse=True):
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, msg_lower):
                return PROPERTY_TYPE_KEYWORDS[keyword]
        return None

    def _extract_location(self, message: str, msg_lower: str):
        """Extract Chennai area/location from known area keyword list."""
        for area in sorted(CHENNAI_LOCATION_KEYWORDS, key=len, reverse=True):
            pattern = r'\b' + re.escape(area) + r'\b'
            if re.search(pattern, msg_lower):
                return area.title()

        # Generic location pattern: "in {place}", "at {place}", "near {place}"
        m = re.search(
            r'\b(?:in|at|near|around)\s+([A-Za-z\s]{3,30}?)(?:\.|,|$|\s+(?:area|locality|zone))',
            msg_lower,
        )
        if m:
            loc = m.group(1).strip().title()
            if len(loc) >= 3:
                return loc
        return None

    def _extract_budget(self, message: str, msg_lower: str):
        """Extract INR or USD budget amounts."""
        m = _RE_BUDGET_INR.search(message)
        if m:
            return m.group(0).strip()
        m = _RE_BUDGET_USD.search(message)
        if m:
            return m.group(0).strip()
        return None

    def _extract_timeline(self, message: str, msg_lower: str):
        """Extract timeline/urgency keywords."""
        for keyword in sorted(TIMELINE_KEYWORDS.keys(), key=len, reverse=True):
            if keyword in msg_lower:
                return TIMELINE_KEYWORDS[keyword]

        # Pattern: "within N months/years"
        m = re.search(r'\bwithin\s+(\d+)\s+(month|months|year|years|week|weeks)\b', msg_lower)
        if m:
            count = m.group(1)
            unit = m.group(2)
            return f"Within {count} {unit}"

        return None

    def _extract_contact_time(self, message: str, msg_lower: str):
        """Extract preferred contact time keywords."""
        for keyword in sorted(CONTACT_TIME_KEYWORDS.keys(), key=len, reverse=True):
            if keyword in msg_lower:
                return CONTACT_TIME_KEYWORDS[keyword]
        return None
