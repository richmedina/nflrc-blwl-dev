from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel

class Post(TimeStampedModel):
    text = models.TextField()
    creator = models.ForeignKey(User)
    subject = models.CharField(max_length=512)
    parent_post = models.ForeignKey('self', blank=True, null=True, related_name='replies')

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def __unicode__(self):
        return self.text
