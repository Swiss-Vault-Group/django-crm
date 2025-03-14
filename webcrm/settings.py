import sys
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

from crm.settings import *          # NOQA
from massmail.settings import *     # NOQA
from common.settings import *       # NOQA
from tasks.settings import *        # NOQA
from voip.settings import *         # NOQA

# ---- Django settings ---- #

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# To get new value of key use code:
# from django.core.management.utils import get_random_secret_key
# print(get_random_secret_key())
SECRET_KEY = os.environ.get('SECRET_KEY', 'j1c=6$s-dh#$ywt@(q4cm=j&0c*!0x!e-qm6k1%yoliec(14tn')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

# Add your hosts to the list.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'NAME': os.environ.get('DB_NAME', 'crm_db'),
        'USER': os.environ.get('DB_USER', 'crm_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'crmpass!'),
        'HOST': os.environ.get('DB_HOST', 'db'),
    }
}


EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'crm@vaultx.ch')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_SUBJECT_PREFIX = os.environ.get('EMAIL_SUBJECT_PREFIX', 'CRM: ')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'noreply@vaultx.ch')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@vaultx.ch')


ADMINS_STR = os.environ.get('ADMINS', '<Admin1>:<admin@vaultx.ch>')
ADMINS = [tuple(admin.split(':')) for admin in ADMINS_STR.split(',')]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

FORMS_URLFIELD_ASSUME_HTTPS = os.environ.get('FORMS_URLFIELD_ASSUME_HTTPS', 'True').lower() == 'true'

# Internationalization
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'en')
LANGUAGES = [
    ('ar', 'Arabic'),
    ('cs', 'Czech'),
    ('de', 'German'),
    ('el', 'Greek'),
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    # ('he', 'Hebrew'),
    ('hi', 'Hindi'),
    ('id', 'Indonesian'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('ko', 'Korean'),
    ('nl', 'Nederlands'),
    ('pl', 'Polish'),
    ('pt-br', 'Portuguese'),
    # ('ro', 'Romanian'),
    ('ru', 'Russian'),
    ('tr', 'Turkish'),
    ('uk', 'Ukrainian'),
    ('vi', 'Vietnamese'),
    ('zh-hans', 'Chinese'),
]

TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')

USE_I18N = os.environ.get('USE_I18N', 'True').lower() == 'true'

USE_TZ = os.environ.get('USE_TZ', 'True').lower() == 'true'

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

LOGIN_URL = os.environ.get('LOGIN_URL', '/admin/login/')

# Application definition
INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crm.apps.CrmConfig',
    'massmail.apps.MassmailConfig',
    'analytics.apps.AnalyticsConfig',
    'help',
    'tasks.apps.TasksConfig',
    'chat.apps.ChatConfig',
    'voip',
    'common.apps.CommonConfig',
    'settings',
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

API_BEARER_TOKEN = os.environ.get('API_BEARER_TOKEN', 'dev')
API_USER_EMAIL = os.environ.get('API_USER_EMAIL', 'api@example.com')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.utils.usermiddleware.UserMiddleware'
]

ROOT_URLCONF = 'webcrm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'webcrm.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

FIXTURE_DIRS = ['tests/fixtures']

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

SITE_ID = int(os.environ.get('SITE_ID', '1'))

SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '0'))  # set to 31536000 for production server
# Set all the following to True for production server
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'False').lower() == 'true'
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'False').lower() == 'true'
SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'False').lower() == 'true'


# ---- CRM settings ---- #

# For more security, replace the url prefixes
# with your own unique value.
SECRET_CRM_PREFIX = os.environ.get('SECRET_CRM_PREFIX', '123/')
SECRET_ADMIN_PREFIX = os.environ.get('SECRET_ADMIN_PREFIX', '456-admin/')
SECRET_LOGIN_PREFIX = os.environ.get('SECRET_LOGIN_PREFIX', '789-login/')

# Specify ip of host to avoid importing emails sent by CRM
CRM_IP = os.environ.get('CRM_IP', "127.0.0.1")

CRM_REPLY_TO = os.environ.get('CRM_REPLY_TO', "['Do not reply' <noreply@vaultx.ch>]").split(',')

# List of addresses to which users are not allowed to send mail.
NOT_ALLOWED_EMAILS = os.environ.get('NOT_ALLOWED_EMAILS', '').split(',') if os.environ.get('NOT_ALLOWED_EMAILS') else []

# List of applications on the main page and in the left sidebar.
APP_ON_INDEX_PAGE = [
    'tasks', 'crm', 'analytics',
    'massmail', 'common', 'settings'
]
MODEL_ON_INDEX_PAGE = {
    'tasks': {
        'app_model_list': ['Task', 'Memo']
    },
    'crm': {
        'app_model_list': [
            'Request', 'Deal', 'Lead', 'Company',
            'CrmEmail', 'Payment', 'Shipment'
        ]
    },
    'analytics': {
        'app_model_list': [
            'IncomeStat', 'RequestStat'
        ]
    },
    'massmail': {
        'app_model_list': [
            'MailingOut', 'EmlMessage'
        ]
    },
    'common': {
        'app_model_list': [
            'UserProfile', 'Reminder'
        ]
    },
    'settings': {
        'app_model_list': [
            'PublicEmailDomain', 'StopPhrase'
        ]
    }
}

# Country VAT value
VAT = float(os.environ.get('VAT', '0'))    # %

# 2-Step Verification Credentials for Google Accounts.
#  OAuth 2.0
CLIENT_ID = os.environ.get('CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', '')
OAUTH2_DATA = {
    'smtp.gmail.com': {
        'scope': os.environ.get('OAUTH2_SCOPE', "https://mail.google.com/"),
        'accounts_base_url': os.environ.get('OAUTH2_ACCOUNTS_BASE_URL', 'https://accounts.google.com'),
        'auth_command': os.environ.get('OAUTH2_AUTH_COMMAND', 'o/oauth2/auth'),
        'token_command': os.environ.get('OAUTH2_TOKEN_COMMAND', 'o/oauth2/token'),
    }
}
# Hardcoded dummy redirect URI for non-web apps.
REDIRECT_URI = os.environ.get('REDIRECT_URI', '')

# Credentials for Google reCAPTCHA.
GOOGLE_RECAPTCHA_SITE_KEY = os.environ.get('GOOGLE_RECAPTCHA_SITE_KEY', '')
GOOGLE_RECAPTCHA_SECRET_KEY = os.environ.get('GOOGLE_RECAPTCHA_SECRET_KEY', '')

GEOIP = os.environ.get('GEOIP', 'False').lower() == 'true'
GEOIP_PATH = Path(os.environ.get('GEOIP_PATH', str(MEDIA_ROOT / 'geodb')))

# For user profile list
SHOW_USER_CURRENT_TIME_ZONE = os.environ.get('SHOW_USER_CURRENT_TIME_ZONE', 'False').lower() == 'true'

NO_NAME_STR = _('Untitled')

# For automated getting currency exchange rate
LOAD_EXCHANGE_RATE = os.environ.get('LOAD_EXCHANGE_RATE', 'False').lower() == 'true'
LOADING_EXCHANGE_RATE_TIME = os.environ.get('LOADING_EXCHANGE_RATE_TIME', "6:30")
LOAD_RATE_BACKEND = os.environ.get('LOAD_RATE_BACKEND', "")  # "crm.backends.<specify_backend>.<specify_class>"

# Ability to mark payments through a representation
MARK_PAYMENTS_THROUGH_REP = os.environ.get('MARK_PAYMENTS_THROUGH_REP', 'False').lower() == 'true'


# Site headers
SITE_TITLE = 'CRM'
ADMIN_HEADER = "ADMIN"
ADMIN_TITLE = "CRM Admin"
INDEX_TITLE = _('Main Menu')


# This is copyright information. Please don't change it!
COPYRIGHT_STRING = "Django-CRM. Copyright (c) 2024"
PROJECT_NAME = "Django-CRM"
PROJECT_SITE = "https://github.com/DjangoCRM/django-crm/"


TESTING = sys.argv[1:2] == ['test']
if TESTING:
    SECURE_SSL_REDIRECT = False
    LANGUAGE_CODE = 'en'
    LANGUAGES = [('en', ''), ('uk', '')]
