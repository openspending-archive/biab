"""
Django settings for biab project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY',
    'd=d5#m7j+l+h5eg5@c&!nz&dpil7$*(peou%h^vj*f+o6vtxqv')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'biab', 'templates'),
    )

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    )


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'captcha',
    'bdpsite',
    'djcelery',
    'kombu.transport.django'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'biab.urls'

WSGI_APPLICATION = 'biab.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

import dj_database_url

DATABASES = {
    }
DATABASES['default'] = dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT= 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'biab', 'static'),
    )
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
    )

LOGIN_URL="/user/login"

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '')
RECAPTCHA_USE_SSL = True


# Amazon S3 configuration
S3_BUCKET = os.environ.get('BIAB_S3_BUCKET', None)
S3_HTTP_URL = os.environ.get('BIAB_S3_HTTP', None)
S3_CSV_PREFIX = os.environ.get('BIAB_S3_CSV_PREFIX', 'csv/')
S3_MODEL_PREFIX = os.environ.get('BIAB_S3_MODEL_PREFIX', 'bdp/')

# API key for OpenSpending uploading
OPENSPENDING_API_KEY = os.environ.get('OPENSPENDING_API_KEY', None)

# helper files for utils
RESOURCES = os.path.join(BASE_DIR, 'utils', 'resources')

# Celery setup
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
BROKER_URL = 'django://'