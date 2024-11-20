import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

SECRET_KEY = '*+uiasgfhfhea(0_=n@c6aacvxcd*xtaassdkjlgvzo'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'elmedi_new_db',
        'USER': 'medet',
        'PASSWORD': 'Astana2022',
        'HOST': 'localhost',
        'PORT': '5432'
    },
    'db_03': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'eitae4ahbae5hiz1Ed',
        'HOST': '10.0.100.3',
        'PORT': '5432'
    },
    #or elmedi_db
    'db_8037': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'elmedi_db',
        'USER': 'medet',
        'PASSWORD': 'dostar1996',
        'HOST': '192.168.100.37',
        'PORT': '5432'
    }
}



STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
