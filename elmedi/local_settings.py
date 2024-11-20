import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

SECRET_KEY = '*+rasda(@$^dg8)yus)*aghfcdpa(0_=n@c6*xtasdasoiumo'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



STATIC_URL = "/static/"
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
