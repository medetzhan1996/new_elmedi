import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
CORS_ORIGIN_ALLOW_ALL = True

SECRET_KEY = 'django-insecure-7^64lw7n^&g5(jzxk8)t@q7z!m2&fjb89ib^sxr9mk!q9hv3v='


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mptt',
    'widget_tweaks',
    'import_export',
    'rest_framework',
    'rest_framework.authtoken',
    'pwa',
    'weasyprint',
    'django_filters',
    'rosetta',
    'parler',

    'account',
    'directory',
    'program_management',
    'import_data',
    'package_service_management',
    'package_icd_management',
    'contract_management',
    'hospital_service_management',
    'customer',
    'document_management',
    'referral_management',
    'invoice_management',
    'hospital_icd_management',
    'promedicine'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'elmedi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH, 'templates')],
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

WSGI_APPLICATION = 'elmedi.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'
LANGUAGES = [
    ('ru', 'Russian'),
    ('az', 'Azerbaijan'),
]


TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
USE_L10N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# Static files (CSS, JavaScript, images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# This is where collected static files will be stored for production.


# URL to use when referring to static files.
# STATIC_URL = '/static/'

# This should only include paths to additional directories you want to use during development.
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),  # Adjust this to the appropriate path.
# ]

#***

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LANGUAGE_CODE = 'ru-ru'
DATE_FORMAT = "Y-m-d"

PWA_APP_NAME = 'elmedi'
PWA_APP_DESCRIPTION = "elmedi"
PWA_APP_DEBUG_MODE = True
PWA_APP_START_URL = 'https://portal.euromedix.org/login/'


LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/account/identify/role'

CUSTOMER_CABINET_URL = os.getenv('CUSTOMER_CABINET_URL')
CUSTOMER_CABINET_TOKEN = os.getenv('CUSTOMER_CABINET_TOKEN')

CSRF_TRUSTED_ORIGINS = [CUSTOMER_CABINET_URL]

PARLER_LANGUAGES = {
    None: (
        {'code': 'ru'},
        {'code': 'az'},
    ),
    'default': {
        'fallback': 'ru',
        'hide_untranslated': False,
    }
}

try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *
