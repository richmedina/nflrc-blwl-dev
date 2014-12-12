from django.db import models

from model_utils.models import TimeStampedModel
class Posting(TimeStampedModel):
	text = models.TextField()
