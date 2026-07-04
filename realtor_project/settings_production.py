"""
Production Settings for Propertism Realty Advisors
Security-hardened configuration for production deployment
"""
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# SCCB-WS-LOCAL-STORAGE-HARD-OVERRIDE-V1
# FORCE local storage - single source of truth
USE_LOCAL_STORAGE = os.getenv("USE_LOCAL_STORAGE") == "1"
print(f"[SCCB] STORAGE MODE: {'LOCAL' if USE_LOCAL_STORAGE else 'S3'}")

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable must be set in production")

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = False

# Production hosts - MUST be configured
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ValueError("DJANGO_ALLOWED_HOSTS environment variable must be set in production")

# Allow EB health checker which hits the EC2 instance IP directly
import urllib.request as _urllib_request
try:
    _ec2_ip = _urllib_request.urlopen(
        'http://169.254.169.254/latest/meta-data/local-ipv4', timeout=1
    ).read().decode()
    ALLOWED_HOSTS.append(_ec2_ip)
except Exception:
    pass

# Application definition
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
            ],
        },
    },
]

WSGI_APPLICATION = 'realtor_project.wsgi.application'

# Database - PostgreSQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'propertism_db'),
        'USER': os.environ.get('DB_USER', 'propertism_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'sslmode': 'require',  # Require SSL for database connections
        }
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Kolkata'  # India timezone
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('ta', 'Tamil'),
    ('hi', 'Hindi'),
]

# Modeltranslation
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'ta', 'hi')
MODELTRANSLATION_FALLBACK_LANGUAGES = ('en',)

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Whitenoise Static Caching Headers (CloudFront Edge caching)
WHITENOISE_MAX_AGE = 31536000  # 1 year cache duration
WHITENOISE_KEEP_ONLY_HASHED_FILES = True

# Media files — SCCB HARD OVERRIDE FOR LOCAL STORAGE
if USE_LOCAL_STORAGE:
    # FORCE local storage - NO S3 AT ALL
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    # Ensure media directory exists
    os.makedirs(MEDIA_ROOT, exist_ok=True)
    # HARD BLOCK S3 VARIABLES - prevent any implicit S3 usage
    AWS_STORAGE_BUCKET_NAME = None
    AWS_S3_CUSTOM_DOMAIN = None
    AWS_S3_REGION_NAME = None
    AWS_ACCESS_KEY_ID = None
    AWS_SECRET_ACCESS_KEY = None
else:
    # S3 storage only if explicitly disabled local storage
    _S3_MEDIA_BUCKET = os.environ.get('AWS_MEDIA_BUCKET_NAME', '').strip()
    _AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID', '').strip()
    _AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '').strip()
    
    if _S3_MEDIA_BUCKET and _AWS_ACCESS_KEY and _AWS_SECRET_KEY:
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        AWS_STORAGE_BUCKET_NAME = _S3_MEDIA_BUCKET
        AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
        AWS_S3_CUSTOM_DOMAIN = f'{_S3_MEDIA_BUCKET}.s3.amazonaws.com'
        AWS_LOCATION = 'media'
        AWS_DEFAULT_ACL = None
        AWS_S3_FILE_OVERWRITE = False
        AWS_QUERYSTRING_AUTH = False
        AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=31536000, public, immutable'}
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
        MEDIA_ROOT = ''
    else:
        # Fallback to local if S3 not configured
        DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
        MEDIA_URL = "/media/"
        MEDIA_ROOT = os.path.join(BASE_DIR, "media")
        os.makedirs(MEDIA_ROOT, exist_ok=True)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# HTTPS/SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# CSRF Protection
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = 'Lax'  # Changed from Strict to prevent admin save issues

# CSRF Trusted Origins - must include exact domains used in production
CSRF_TRUSTED_ORIGINS = [
    'https://propertism.in',
    'https://www.propertism.in',
]

# Session Security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Referrer Policy
SECURE_REFERRER_POLICY = 'same-origin'

# ==============================================================================
# CORS SETTINGS
# ==============================================================================

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ==============================================================================
# REST FRAMEWORK & JWT
# ==============================================================================

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ==============================================================================
# LOGGING
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# ==============================================================================
# EMAIL CONFIGURATION
# ==============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'tamil@propertism.in'
SERVER_EMAIL = 'tamil@propertism.in'
ADMIN_EMAIL = 'info@propertism.in'

# Notification recipients — all inquiry/lead alerts go to both inboxes in production
ADMIN_EMAILS = ['info@propertism.in', 'propertism.tamil@gmail.com', 'tamil@propertism.in']

# Canonical host configurations
CANONICAL_HOST = os.environ.get('CANONICAL_HOST', 'www.propertism.in')
CANONICAL_SCHEME = os.environ.get('CANONICAL_SCHEME', 'https')
CANONICAL_REDIRECT_HOSTS = os.environ.get(
    'CANONICAL_REDIRECT_HOSTS',
    'propertism.in,propertism.com,www.propertism.com'
).split(',')

# Microsoft Clarity Project ID
CLARITY_PROJECT_ID = os.environ.get('CLARITY_PROJECT_ID', '')

# ==============================================================================
# ADMIN SECURITY
# ==============================================================================

ADMINS = [
    ('Admin', os.environ.get('ADMIN_EMAIL', 'admin@propertism.com')),
]
MANAGERS = ADMINS

# ==============================================================================
# FILE UPLOAD SECURITY
# ==============================================================================

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx']

# ==============================================================================
# CACHE CONFIGURATION
# ==============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'propertism',
        'TIMEOUT': 300,
    }
}

# ==============================================================================
# PERFORMANCE
# ==============================================================================

# Database connection pooling
CONN_MAX_AGE = 600

# Template caching
if not DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]

# WhatsApp Cloud API Configuration
WHATSAPP_PHONE_ID = os.environ.get('WHATSAPP_PHONE_ID', '')
WHATSAPP_ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN', '')
WHATSAPP_ADMIN_PHONE = os.environ.get('WHATSAPP_ADMIN_PHONE', '') # with country code, no +
WHATSAPP_APP_ID = os.environ.get('WHATSAPP_APP_ID', '')
WHATSAPP_APP_SECRET = os.environ.get('WHATSAPP_APP_SECRET', '')

# Tamilselvan Profile Contact Settings
TAMILSELVAN_EMAIL_1 = os.environ.get('TAMILSELVAN_EMAIL_1', 'info@propertism.in')
TAMILSELVAN_EMAIL_2 = os.environ.get('TAMILSELVAN_EMAIL_2', 'propertism.tamil@gmail.com')

