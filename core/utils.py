# utils.py
from django.conf import settings

from .models import Whitelist

def nflrc_auth_allowed(backend, details, response, *args, **kwargs):
	# This method is designed to be called before 'social.pipeline.social_auth.auth_allowed' in the social_auth pipeline. 
	# The method is referenced from the settings. It populates the whitelist from a db query rather that in the clear in the settings file.
	# See: http://python-social-auth.readthedocs.org/en/latest/pipeline.html?highlight=pipelines for more information about this.
    
    settings.SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = [i.email_addr for i in Whitelist.objects.all()]
