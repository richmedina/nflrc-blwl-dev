from django.db import models

from model_utils.models import TimeStampedModel

class Whitelist(TimeStampedModel):
	email_addr = models.EmailField(max_length=254)

	def __unicode__(self):
		return self.email_addr


