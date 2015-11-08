# dev.py
from .base import *


SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += (
    'debug_toolbar',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_DIR.child('pbll-dev.sqlite3'),
    }
}

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']  # This is the Client ID (not a key)

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = []
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-forbidden/'

LOGIN_URL = '/login/google-oauth2'
LOGIN_REDIRECT_URL = '/'

MEDIA_ROOT = '/Library/WebServer/Documents/media'
MEDIA_URL = 'http://localhost/media/'
