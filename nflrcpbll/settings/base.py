"""
Django settings for nflrcpbll project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(3)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECRET_KEY IS NOT DEFINED IN BASE. Must be set in relavant runtime environment/context

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'quiz',
    'multichoice',
    'true_false',
    'essay',

    'lessons',
    'core',

    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'nflrcpbll.urls'

WSGI_APPLICATION = 'nflrcpbll.wsgi.application'


# Database not set here
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Pacific/Honolulu'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = (PROJECT_DIR.child('templates'),)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATICFILES_DIRS = (PROJECT_DIR.child('static'),)


STATIC_URL = '/static/'
