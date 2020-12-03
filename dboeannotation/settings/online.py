from .base import *



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o#hz35slckzb)3xqwezhb)wc_0=d7xzuyef0zsket0ae8bi@us'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dboeannotation',
        'USER': 'dboeannotation',
        'PASSWORD': 'G47jVAgg51UV',
        #'HOST': 'helios.arz.oeaw.ac.at',
        #'PORT': '5432',
        'HOST': 'localhost',
        'PORT': '4200',
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dboeannotation',
        'USER': 'dboeannotation',
        'PASSWORD': 'dboeannotation',
        #'HOST': 'helios.arz.oeaw.ac.at',
        #'PORT': '5432',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

ES_DBOE = 'https://walk-want-grew.acdh.oeaw.ac.at/'