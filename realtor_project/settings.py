# Django settings for realtor_project
import os
from pathlib import Path
from urllib.parse import unquote, urlparse

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass  # python-dotenv not installed, will use system environment variables

# Environment detection
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')
IS_LOCAL_DEVELOPMENT = DJANGO_ENV == 'development'


def _get_csv_env(*names, default=None):
    for name in names:
        value = os.environ.get(name)
        if value:
            return [item.strip() for item in value.split(',') if item.strip()]
    return default if default is not None else []


def _get_https_origins_from_hosts(hosts):
    origins = []
    for host in hosts:
        normalized = (host or "").strip()
        if not normalized or normalized == "*":
            continue
        if normalized.startswith("."):
            normalized = "*" + normalized
        if "://" not in normalized:
            normalized = f"https://{normalized}"
        origins.append(normalized)
    return list(dict.fromkeys(origins))


def _get_env_value(*names):
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _get_bool_env(*names, default=False):
    for name in names:
        value = os.environ.get(name)
        if value is None:
            continue
        return value.strip().lower() in {'1', 'true', 'yes', 'on'}
    return default


def _database_config_from_url(database_url):
    parsed = urlparse(database_url)
    engine_map = {
        'postgres': 'django.db.backends.postgresql',
        'postgresql': 'django.db.backends.postgresql',
        'pgsql': 'django.db.backends.postgresql',
    }
    engine = engine_map.get(parsed.scheme)
    if not engine:
        return None
    config = {
        'ENGINE': engine,
        'NAME': parsed.path.lstrip('/'),
        'USER': unquote(parsed.username or ''),
        'PASSWORD': unquote(parsed.password or ''),
        'HOST': parsed.hostname or '',
        'PORT': str(parsed.port or '5432'),
    }
    sslmode = _get_env_value('POSTGRES_SSLMODE', 'DATABASE_SSLMODE')
    if sslmode:
        config['OPTIONS'] = {'sslmode': sslmode}
    return config


def _get_local_postgres_config():
    database_url = _get_env_value('DATABASE_URL', 'LOCAL_DATABASE_URL')
    if database_url:
        return _database_config_from_url(database_url)

    name = _get_env_value('POSTGRES_DB', 'LOCAL_POSTGRES_DB')
    if not name:
        return None

    config = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': name,
        'USER': _get_env_value('POSTGRES_USER', 'LOCAL_POSTGRES_USER') or '',
        'PASSWORD': _get_env_value('POSTGRES_PASSWORD', 'LOCAL_POSTGRES_PASSWORD') or '',
        'HOST': _get_env_value('POSTGRES_HOST', 'LOCAL_POSTGRES_HOST') or '127.0.0.1',
        'PORT': _get_env_value('POSTGRES_PORT', 'LOCAL_POSTGRES_PORT') or '5432',
    }
    sslmode = _get_env_value('POSTGRES_SSLMODE', 'DATABASE_SSLMODE')
    if sslmode:
        config['OPTIONS'] = {'sslmode': sslmode}
    return config

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = (
    os.environ.get('DJANGO_SECRET_KEY')
    or os.environ.get('SECRET_KEY')
    or 'django-insecure-realtor-project-secret-key-change-in-production'
)

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Allowed hosts
ALLOWED_HOSTS = _get_csv_env('DJANGO_ALLOWED_HOSTS', 'ALLOWED_HOSTS', default=['*'])
# Add localhost and 127.0.0.1 for local development
if DEBUG or IS_LOCAL_DEVELOPMENT:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

CANONICAL_HOST = os.environ.get('CANONICAL_HOST', 'www.propertism.in')
CANONICAL_SCHEME = os.environ.get('CANONICAL_SCHEME', 'https')
CANONICAL_REDIRECT_HOSTS = _get_csv_env(
    'CANONICAL_REDIRECT_HOSTS',
    default=['propertism.in', 'propertism.com', 'www.propertism.com'],
)

INSTALLED_APPS = [
    'modeltranslation',  # Must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',  # For SEO sitemap generation
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    # django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # Project apps
    'properties.apps.PropertiesConfig',
    'users.apps.UsersConfig',
    'search.apps.SearchConfig',
    'uilayers.apps.UilayersConfig',
    'content.apps.ContentConfig',
    'chat.apps.ChatConfig',
    'nri_assist.apps.NriAssistConfig',
]

SITE_ID = 1

MIDDLEWARE = [
    'content.middleware.HealthCheckMiddleware',  # Handle health checks before ALLOWED_HOSTS
    'content.middleware.CanonicalDomainRedirectMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files efficiently
    'django.middleware.gzip.GZipMiddleware',  # Enable gzip compression
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'content.middleware.AdminAccessMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'realtor_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'uilayers' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'content.context_processors.site_content',
            ],
        },
    },
]

WSGI_APPLICATION = 'realtor_project.wsgi.application'

# Database selection
# 1. Production RDS configuration on Elastic Beanstalk
# 2. Optional local PostgreSQL via .env
# 3. SQLite fallback for local development
LOCAL_POSTGRES_DATABASE = _get_local_postgres_config()
if 'RDS_DB_NAME' in os.environ:
    database_config = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
    sslmode = _get_env_value('POSTGRES_SSLMODE', 'DATABASE_SSLMODE')
    if sslmode:
        database_config['OPTIONS'] = {'sslmode': sslmode}
    DATABASES = {'default': database_config}
elif LOCAL_POSTGRES_DATABASE:
    DATABASES = {
        'default': LOCAL_POSTGRES_DATABASE,
    }
else:
    # SQLite remains the default local fallback when no PostgreSQL env vars are set
    DB_PATH = os.environ.get('DB_PATH', str(BASE_DIR / 'db.sqlite3'))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DB_PATH,
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

APPEND_SLASH = True

# ==============================================================================
# STATIC FILES CONFIGURATION (SCCB-44)
# ==============================================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration for production static file serving
# Using default storage to avoid manifest issues on custom domain
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
# MEDIA FILES CONFIGURATION (SCCB-44)
# ==============================================================================

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

# S3 media storage — activated whenever AWS_MEDIA_BUCKET_NAME env var is set
_S3_MEDIA_BUCKET = os.environ.get('AWS_MEDIA_BUCKET_NAME', '')
if _S3_MEDIA_BUCKET:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = _S3_MEDIA_BUCKET
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{_S3_MEDIA_BUCKET}.s3.amazonaws.com'
    # AWS_LOCATION removed — upload_to paths already include directory structure
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
    MEDIA_ROOT = ''
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

# Allowed file extensions for uploads
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization (Multi-language support)
LANGUAGES = [
    ('en', 'English'),
    ('ta', 'Tamil'),
    ('hi', 'Hindi'),
]

LANGUAGE_CODE = 'en'

# Modeltranslation settings
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'ta', 'hi')
MODELTRANSLATION_FALLBACK_LANGUAGES = ('en',)

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:19000",
    "http://127.0.0.1:5173",
]

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# JWT Settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# ==============================================================================
# ALLAUTH — Google OAuth (SCCB-PROP-NRIASSIST-0805)
# ==============================================================================

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID', ''),
            'secret': os.environ.get('GOOGLE_CLIENT_SECRET', ''),
            'key': '',
        },
    }
}

LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/accounts/login/'
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

# SCCB-SEC-PRT-1510: Close public signup — Google OAuth is the only registration path.
ACCOUNT_ADAPTER = 'users.adapters.PropertismAccountAdapter'  # blocks /accounts/signup/
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # belt-and-suspenders: verify if ever reopened
SOCIALACCOUNT_AUTO_SIGNUP = True        # Google OAuth registration remains open
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'  # Google already verifies — skip allauth re-check
SOCIALACCOUNT_LOGIN_ON_GET = True           # drawer button goes direct to Google — skip login page
SOCIALACCOUNT_ADAPTER = 'users.adapters.AdminOnlySocialAccountAdapter'

if not DEBUG:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# Security headers (enabled in all environments)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'SAMEORIGIN'  # Allow framing from same origin

# CSRF Protection
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'  # Lax for development, Strict for production
# Add trusted origins for custom domain (HTTPS after SSL is configured)
CSRF_TRUSTED_ORIGINS = _get_csv_env('CSRF_TRUSTED_ORIGINS', default=[
    'https://propertism.in',
    'https://www.propertism.in',
    'https://d1yv5od4i0bho.cloudfront.net',
    'http://propertism-prod-2026.us-east-1.elasticbeanstalk.com',
])

# Session Security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 86400  # 24 hours

# Password validation - enforce strong passwords
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# File upload security
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE

# Production-specific security settings
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True

    # Enable strict HTTPS-only behavior only after SSL is actually configured.
    if _get_bool_env('ENABLE_HTTPS', 'FORCE_HTTPS', default=False):
        SECURE_SSL_REDIRECT = True
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True
        SECURE_HSTS_SECONDS = 31536000
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True
    
    # Stricter settings for production
    CSRF_COOKIE_SAMESITE = 'Lax'  # Changed from Strict to prevent admin form submission issues
    SESSION_COOKIE_SAMESITE = 'Strict'
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    X_FRAME_OPTIONS = 'DENY'

    if not CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS = _get_https_origins_from_hosts(ALLOWED_HOSTS)

# ==============================================================================
# EMAIL CONFIGURATION
# ==============================================================================

# Email backend configuration
if DEBUG:
    # Console backend for development (prints emails to console)
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # SMTP backend for production
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Gmail SMTP Configuration
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Default email addresses
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'propertism.tamil@gmail.com')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'propertism.tamil@gmail.com')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'info@propertism.in')

# Notification recipients — all inquiry/lead alerts go to both inboxes
_extra_recipients = os.environ.get('EXTRA_NOTIFICATION_EMAIL', 'propertism.tamil@gmail.com')
ADMIN_EMAILS = list({ADMIN_EMAIL, _extra_recipients})  # deduplicates if same address

# Email timeout (seconds)
EMAIL_TIMEOUT = 10

# ==============================================================================
# ADMIN CUSTOMIZATION
# ==============================================================================

# Custom admin URL (can be changed via environment variable)
ADMIN_URL = os.environ.get('ADMIN_URL', 'admin')

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================

# Simplified logging for production - console only
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


# ==============================================================================
# PERFORMANCE OPTIMIZATION
# ==============================================================================

# Browser caching for static files (handled by nginx)
# Removed conflicting STATICFILES_STORAGE setting

# Gzip compression settings (handled by nginx)
GZIP_CONTENT_TYPES = (
    'text/css',
    'text/javascript',
    'application/javascript',
    'application/x-javascript',
    'text/html',
    'text/plain',
    'application/json',
    'application/xml',
    'text/xml',
)

# Data upload settings (already defined above, but ensuring they're set)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# WhatsApp Cloud API Configuration
WHATSAPP_PHONE_ID = os.environ.get('WHATSAPP_PHONE_ID', '')
WHATSAPP_ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN', '')
WHATSAPP_ADMIN_PHONE = os.environ.get('WHATSAPP_ADMIN_PHONE', '') # with country code, no +

# ===== SCCB: SURGICAL STORAGE OVERRIDE =====
# This MUST be at the very end to override any previous storage settings

USE_LOCAL_STORAGE = os.getenv("USE_LOCAL_STORAGE") == "1"

if USE_LOCAL_STORAGE:
    print("✅ SCCB STORAGE MODE: LOCAL (S3 DISABLED)")
    
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    
    # HARD NULLIFY S3 - prevents ANY S3 usage
    AWS_STORAGE_BUCKET_NAME = None
    AWS_S3_CUSTOM_DOMAIN = None
