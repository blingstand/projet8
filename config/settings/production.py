from . import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


SECRET_KEY = '%2liguu(w2ag#^ys)e_wb6-_r1g5%hry*f+beob_#=(_36b+(6'
DEBUG = True 
ALLOWED_HOSTS = ['35.180.64.180']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # adaptateur postgresql
        'NAME': 'purebeurre',
        'USER': 'adi',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

sentry_sdk.init(
    dsn="https://05e89a4df1b24054b90c8fff6ea1a85f@o388096.ingest.sentry.io/5240594",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
