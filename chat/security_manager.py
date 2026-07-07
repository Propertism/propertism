"""
chat/security_manager.py — M2.14 Security, Authorization & Platform Governance Framework.
Implements SecurityPolicyEngine, SecurityAuditManager, RequestValidator, InputSanitizer,
OutputValidator, RateLimiter, AbuseDetector, AuthorizationManager, and SecurityManager.
"""
import re
import time
import html
import logging
from typing import Any, Dict, List, Optional, Tuple
from chat.models import SecurityEvent, SecurityPolicy

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Security Policy Engine
# ─────────────────────────────────────────────────────────────────────────────

class SecurityPolicyEngine:
    """
    Loads, caches, and evaluates configuration-driven security policies.
    Provides typed value retrieval for limits, thresholds, rules, and constraints.
    """
    _cache: Dict[str, Any] = {}

    @classmethod
    def load_policies(cls) -> None:
        """Loads all active policies into the in-memory cache."""
        try:
            policies = SecurityPolicy.objects.filter(is_active=True)
            cls._cache = {p.policy_key: p.value for p in policies}
        except Exception as exc:
            logger.exception(f"Failed to load security policies: {exc}")

    @classmethod
    def get_policy(cls, key: str, default: Any = None) -> Optional[str]:
        """Returns the raw string value of a policy key."""
        if not cls._cache:
            cls.load_policies()
        return cls._cache.get(key, default)

    @classmethod
    def get_int(cls, key: str, default: int = 0) -> int:
        val = cls.get_policy(key)
        if val is None:
            return default
        try:
            return int(val)
        except (ValueError, TypeError):
            return default

    @classmethod
    def get_bool(cls, key: str, default: bool = False) -> bool:
        val = cls.get_policy(key)
        if val is None:
            return default
        return str(val).strip().lower() in ('true', '1', 'yes', 'on')

    @classmethod
    def clear_cache(cls) -> None:
        cls._cache.clear()


# ─────────────────────────────────────────────────────────────────────────────
# 2. Security Audit Manager
# ─────────────────────────────────────────────────────────────────────────────

class SecurityAuditManager:
    """
    Writes immutable, append-only SecurityEvent records.
    No update or delete operations are permitted.
    """

    def log_event(
        self,
        event_type: str,
        severity: str = 'info',
        source_ip: str = '',
        session_id: str = '',
        request_path: str = '',
        details: Optional[Dict[str, Any]] = None
    ) -> SecurityEvent:
        try:
            evt = SecurityEvent.objects.create(
                event_type=event_type,
                severity=severity,
                source_ip=source_ip,
                session_id=session_id,
                request_path=request_path,
                details=details or {}
            )
            return evt
        except Exception as exc:
            logger.exception(f"Failed to log security event {event_type}: {exc}")
            return SecurityEvent(event_type=event_type, severity=severity)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Request Validator
# ─────────────────────────────────────────────────────────────────────────────

class RequestValidator:
    """
    Pre-orchestration request validation.
    Enforces maximum request length, required fields, and content-type constraints.
    """

    DEFAULT_MAX_REQUEST_LENGTH = 5000

    def validate(self, request_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validates the incoming request payload.
        Returns (is_valid, list_of_violation_messages).
        """
        violations = []

        # 1. Maximum request length
        max_len = SecurityPolicyEngine.get_int('max_request_length', self.DEFAULT_MAX_REQUEST_LENGTH)
        message_text = request_data.get('message_text', '')
        if len(str(message_text)) > max_len:
            violations.append(f"Message exceeds maximum length of {max_len} characters.")

        # 2. Required fields
        if not message_text or not str(message_text).strip():
            violations.append("Message text is required and cannot be empty.")

        # 3. Session ID presence
        session_id = request_data.get('session_id', '')
        if not session_id or not str(session_id).strip():
            violations.append("Session ID is required.")

        return len(violations) == 0, violations


# ─────────────────────────────────────────────────────────────────────────────
# 4. Input Sanitizer
# ─────────────────────────────────────────────────────────────────────────────

class InputSanitizer:
    """
    Cleans and sanitizes incoming user message text.
    Strips HTML, blocks script injection, detects SQL injection patterns,
    validates URLs, and removes control characters.
    """

    # Script injection patterns
    SCRIPT_PATTERNS = [
        re.compile(r'<\s*script', re.IGNORECASE),
        re.compile(r'javascript\s*:', re.IGNORECASE),
        re.compile(r'on\w+\s*=', re.IGNORECASE),       # onclick=, onload=, etc.
        re.compile(r'<\s*iframe', re.IGNORECASE),
        re.compile(r'<\s*object', re.IGNORECASE),
        re.compile(r'<\s*embed', re.IGNORECASE),
        re.compile(r'expression\s*\(', re.IGNORECASE),  # CSS expression()
        re.compile(r'vbscript\s*:', re.IGNORECASE),
    ]

    # SQL injection patterns
    SQL_PATTERNS = [
        re.compile(r"('|\")\s*;\s*(DROP|DELETE|UPDATE|INSERT|ALTER|EXEC)", re.IGNORECASE),
        re.compile(r'UNION\s+(ALL\s+)?SELECT', re.IGNORECASE),
        re.compile(r'--\s*$', re.MULTILINE),
        re.compile(r'/\*.*?\*/', re.DOTALL),
        re.compile(r';\s*(DROP|DELETE|TRUNCATE)\s+TABLE', re.IGNORECASE),
    ]

    # Dangerous URL schemes
    DANGEROUS_SCHEMES = ['data:', 'javascript:', 'vbscript:']

    # HTML tag pattern
    HTML_TAG_PATTERN = re.compile(r'<[^>]+>')

    # Control character pattern (excluding newlines and tabs)
    CONTROL_CHAR_PATTERN = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')

    def sanitize(self, text: str) -> Tuple[str, bool, List[str]]:
        """
        Sanitizes input text.
        Returns (sanitized_text, has_threats, list_of_threat_descriptions).
        """
        threats = []

        if not text:
            return '', False, threats

        # 1. Script injection detection
        for pattern in self.SCRIPT_PATTERNS:
            if pattern.search(text):
                threats.append(f"Script injection pattern detected: {pattern.pattern}")

        # 2. SQL injection detection
        for pattern in self.SQL_PATTERNS:
            if pattern.search(text):
                threats.append(f"SQL injection pattern detected: {pattern.pattern}")

        # 3. Dangerous URL scheme detection
        text_lower = text.lower()
        for scheme in self.DANGEROUS_SCHEMES:
            if scheme in text_lower:
                threats.append(f"Dangerous URL scheme detected: {scheme}")

        # 4. Strip HTML tags
        sanitized = self.HTML_TAG_PATTERN.sub('', text)

        # 5. HTML entity decoding for safety
        sanitized = html.unescape(sanitized)

        # 6. Remove control characters
        sanitized = self.CONTROL_CHAR_PATTERN.sub('', sanitized)

        # 7. Trim excessive whitespace
        sanitized = sanitized.strip()

        has_threats = len(threats) > 0
        return sanitized, has_threats, threats


# ─────────────────────────────────────────────────────────────────────────────
# 5. Output Validator
# ─────────────────────────────────────────────────────────────────────────────

class OutputValidator:
    """
    Post-composition validation for outgoing responses.
    Ensures no internal data leaks and validates response payload integrity.
    """

    # Patterns that should never appear in customer-facing responses
    INTERNAL_LEAK_PATTERNS = [
        re.compile(r'Traceback \(most recent call last\)', re.IGNORECASE),
        re.compile(r'File "[^"]+\.py"', re.IGNORECASE),
        re.compile(r'django\.db\.', re.IGNORECASE),
        re.compile(r'OperationalError', re.IGNORECASE),
        re.compile(r'IntegrityError', re.IGNORECASE),
        re.compile(r'SECRET_KEY', re.IGNORECASE),
        re.compile(r'DATABASE_URL', re.IGNORECASE),
        re.compile(r'password\s*=\s*["\'][^"\']+["\']', re.IGNORECASE),
    ]

    def validate(self, response_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validates outgoing response payload.
        Returns (is_safe, list_of_issues).
        """
        issues = []

        # Convert response to string for scanning
        response_str = str(response_data)

        # 1. Internal data leak check
        for pattern in self.INTERNAL_LEAK_PATTERNS:
            if pattern.search(response_str):
                issues.append(f"Internal data leak detected: {pattern.pattern}")

        return len(issues) == 0, issues


# ─────────────────────────────────────────────────────────────────────────────
# 6. Rate Limiter
# ─────────────────────────────────────────────────────────────────────────────

class RateLimiter:
    """
    Sliding window rate limiter.
    Tracks request counts per session within configurable time windows.
    """
    _request_log: Dict[str, List[float]] = {}

    DEFAULT_RATE_LIMIT = 60          # requests per window
    DEFAULT_WINDOW_SECONDS = 60     # 1-minute window

    @classmethod
    def check_rate(cls, session_id: str) -> Tuple[bool, int]:
        """
        Checks if the session has exceeded the rate limit.
        Returns (is_allowed, current_count_in_window).
        """
        max_requests = SecurityPolicyEngine.get_int('rate_limit_requests_per_minute', cls.DEFAULT_RATE_LIMIT)
        window_seconds = SecurityPolicyEngine.get_int('rate_limit_window_seconds', cls.DEFAULT_WINDOW_SECONDS)

        now = time.time()
        window_start = now - window_seconds

        # Initialize or clean stale entries
        if session_id not in cls._request_log:
            cls._request_log[session_id] = []

        # Remove timestamps outside the window
        cls._request_log[session_id] = [
            ts for ts in cls._request_log[session_id]
            if ts > window_start
        ]

        current_count = len(cls._request_log[session_id])

        if current_count >= max_requests:
            return False, current_count

        # Record this request
        cls._request_log[session_id].append(now)
        return True, current_count + 1

    @classmethod
    def reset(cls, session_id: Optional[str] = None) -> None:
        """Resets rate limit tracking. If session_id is None, resets all."""
        if session_id:
            cls._request_log.pop(session_id, None)
        else:
            cls._request_log.clear()


# ─────────────────────────────────────────────────────────────────────────────
# 7. Abuse Detector
# ─────────────────────────────────────────────────────────────────────────────

class AbuseDetector:
    """
    Pattern-based abuse detection.
    Monitors repeated identical messages and rapid-fire request bursts.
    """
    _message_history: Dict[str, List[Dict[str, Any]]] = {}

    DEFAULT_DUPLICATE_THRESHOLD = 5
    DEFAULT_BURST_THRESHOLD = 10
    DEFAULT_BURST_WINDOW_SECONDS = 5

    @classmethod
    def check_abuse(cls, session_id: str, message_text: str) -> Tuple[bool, Optional[str]]:
        """
        Checks for abuse patterns.
        Returns (is_abusive, abuse_reason).
        """
        now = time.time()

        if session_id not in cls._message_history:
            cls._message_history[session_id] = []

        cls._message_history[session_id].append({
            'text': message_text,
            'timestamp': now
        })

        # 1. Duplicate message detection
        dup_threshold = SecurityPolicyEngine.get_int(
            'abuse_duplicate_threshold', cls.DEFAULT_DUPLICATE_THRESHOLD
        )
        recent_messages = cls._message_history[session_id][-dup_threshold:]
        if len(recent_messages) >= dup_threshold:
            texts = [m['text'] for m in recent_messages]
            if len(set(texts)) == 1:
                return True, f"Repeated identical message detected ({dup_threshold} times)."

        # 2. Rapid-fire burst detection
        burst_threshold = SecurityPolicyEngine.get_int(
            'abuse_burst_threshold', cls.DEFAULT_BURST_THRESHOLD
        )
        burst_window = SecurityPolicyEngine.get_int(
            'abuse_burst_window_seconds', cls.DEFAULT_BURST_WINDOW_SECONDS
        )
        window_start = now - burst_window
        burst_count = sum(
            1 for m in cls._message_history[session_id]
            if m['timestamp'] > window_start
        )
        if burst_count >= burst_threshold:
            return True, f"Rapid-fire burst detected ({burst_count} messages in {burst_window}s)."

        # 3. Trim old history (keep last 100 entries per session)
        if len(cls._message_history[session_id]) > 100:
            cls._message_history[session_id] = cls._message_history[session_id][-100:]

        return False, None

    @classmethod
    def reset(cls, session_id: Optional[str] = None) -> None:
        """Resets abuse tracking. If session_id is None, resets all."""
        if session_id:
            cls._message_history.pop(session_id, None)
        else:
            cls._message_history.clear()


# ─────────────────────────────────────────────────────────────────────────────
# 8. Authorization Manager
# ─────────────────────────────────────────────────────────────────────────────

class AuthorizationManager:
    """
    Centralized authorization decisions for actions, navigation,
    configuration access, and administrative operations.
    """

    def authorize_action(self, action_type: str, context: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """
        Evaluates whether an action is authorized.
        Returns (is_authorized, reason).
        """
        context = context or {}

        # 1. Check if action type is explicitly blocked by policy
        blocked_actions_str = SecurityPolicyEngine.get_policy('blocked_action_types', '')
        if blocked_actions_str:
            blocked_list = [a.strip().lower() for a in blocked_actions_str.split(',') if a.strip()]
            if action_type.lower() in blocked_list:
                return False, f"Action '{action_type}' is blocked by security policy."

        # 2. Check if restricted navigation paths apply
        if action_type == 'navigation':
            restricted_paths_str = SecurityPolicyEngine.get_policy('restricted_navigation_paths', '')
            if restricted_paths_str:
                restricted = [p.strip() for p in restricted_paths_str.split(',') if p.strip()]
                target_path = context.get('target_path', '')
                if target_path in restricted:
                    return False, f"Navigation to '{target_path}' is restricted by security policy."

        # 3. Check configuration access authorization
        if action_type == 'configuration_access':
            config_access_enabled = SecurityPolicyEngine.get_bool('allow_configuration_access', True)
            if not config_access_enabled:
                return False, "Configuration access is disabled by security policy."

        # 4. Check administrative operation authorization
        if action_type == 'admin_operation':
            admin_enabled = SecurityPolicyEngine.get_bool('allow_admin_operations', True)
            if not admin_enabled:
                return False, "Administrative operations are disabled by security policy."

        return True, "Authorized."

    def authorize_request(self, request_path: str, context: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """
        Evaluates whether a request path is authorized.
        Returns (is_authorized, reason).
        """
        # Check API path restrictions
        restricted_apis_str = SecurityPolicyEngine.get_policy('restricted_api_paths', '')
        if restricted_apis_str:
            restricted = [p.strip() for p in restricted_apis_str.split(',') if p.strip()]
            if request_path in restricted:
                return False, f"API path '{request_path}' is restricted."

        return True, "Authorized."


# ─────────────────────────────────────────────────────────────────────────────
# 9. Security Manager (Facade)
# ─────────────────────────────────────────────────────────────────────────────

class SecurityManager:
    """
    Top-level security facade integrating all security subsystems.
    Single entry point for request validation, output validation,
    authorization, and security event logging.
    """

    def __init__(self):
        self.audit = SecurityAuditManager()
        self.request_validator = RequestValidator()
        self.input_sanitizer = InputSanitizer()
        self.output_validator = OutputValidator()
        self.rate_limiter = RateLimiter()
        self.abuse_detector = AbuseDetector()
        self.authorization = AuthorizationManager()
        self.policy_engine = SecurityPolicyEngine()

    def validate_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Full pre-orchestration security validation pipeline.
        Returns a result dict with is_valid, sanitized_message, and any violations.
        """
        session_id = request_data.get('session_id', '')
        message_text = request_data.get('message_text', '')
        source_ip = request_data.get('source_ip', '')
        request_path = request_data.get('request_path', '')

        result = {
            'is_valid': True,
            'sanitized_message': message_text,
            'violations': [],
            'threats': [],
            'rate_limited': False,
            'abuse_detected': False,
        }

        # 1. Request validation
        req_valid, req_violations = self.request_validator.validate(request_data)
        if not req_valid:
            result['is_valid'] = False
            result['violations'].extend(req_violations)
            self.audit.log_event(
                event_type='invalid_request',
                severity='warning',
                source_ip=source_ip,
                session_id=session_id,
                request_path=request_path,
                details={'violations': req_violations}
            )

        # 2. Input sanitization
        sanitized, has_threats, threats = self.input_sanitizer.sanitize(message_text)
        result['sanitized_message'] = sanitized
        if has_threats:
            result['threats'] = threats
            self.audit.log_event(
                event_type='policy_violation',
                severity='warning',
                source_ip=source_ip,
                session_id=session_id,
                request_path=request_path,
                details={'threats': threats, 'original_text': message_text[:200]}
            )

        # 3. Rate limiting
        rate_allowed, rate_count = self.rate_limiter.check_rate(session_id)
        if not rate_allowed:
            result['is_valid'] = False
            result['rate_limited'] = True
            result['violations'].append(f"Rate limit exceeded ({rate_count} requests).")
            self.audit.log_event(
                event_type='rate_limit_triggered',
                severity='warning',
                source_ip=source_ip,
                session_id=session_id,
                request_path=request_path,
                details={'request_count': rate_count}
            )

        # 4. Abuse detection
        is_abusive, abuse_reason = self.abuse_detector.check_abuse(session_id, message_text)
        if is_abusive:
            result['is_valid'] = False
            result['abuse_detected'] = True
            result['violations'].append(abuse_reason)
            self.audit.log_event(
                event_type='abuse_detected',
                severity='critical',
                source_ip=source_ip,
                session_id=session_id,
                request_path=request_path,
                details={'reason': abuse_reason}
            )

        return result

    def validate_output(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post-composition output validation.
        Returns result with is_safe and any issues detected.
        """
        is_safe, issues = self.output_validator.validate(response_data)
        result = {
            'is_safe': is_safe,
            'issues': issues,
        }
        if not is_safe:
            self.audit.log_event(
                event_type='security_exception',
                severity='critical',
                details={'output_issues': issues}
            )
        return result

    def authorize(self, action_type: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Centralized authorization check.
        Returns result with is_authorized and reason.
        """
        is_authorized, reason = self.authorization.authorize_action(action_type, context)
        if not is_authorized:
            self.audit.log_event(
                event_type='authorization_failure',
                severity='warning',
                details={'action_type': action_type, 'reason': reason, 'context': context or {}}
            )
        return {'is_authorized': is_authorized, 'reason': reason}

    def log_security_event(
        self,
        event_type: str,
        severity: str = 'info',
        source_ip: str = '',
        session_id: str = '',
        request_path: str = '',
        details: Optional[Dict[str, Any]] = None
    ) -> SecurityEvent:
        """Convenience proxy for direct security event logging."""
        return self.audit.log_event(
            event_type=event_type,
            severity=severity,
            source_ip=source_ip,
            session_id=session_id,
            request_path=request_path,
            details=details
        )
