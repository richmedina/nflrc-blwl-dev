from django.db import models

from model_utils.models import TimeStampedModel

PARTICIPANT_TYPES = (
	('opt1', 'Option 1'),
	('opt2', 'Option 2'),
	('staff', 'Staff')
)

class Whitelist(TimeStampedModel):
	email_addr = models.EmailField(max_length=254)
	honor_agreement = models.BooleanField(default=False)
	participant_type = models.CharField(max_length=8, choices=PARTICIPANT_TYPES, default='opt1')

	def __unicode__(self):
		return self.email_addr
