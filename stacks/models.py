from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

from model_utils.models import TimeStampedModel


class Stack(TimeStampedModel):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Stack, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('stack', args=[str(self.slug)])


class Card(TimeStampedModel):
    title = models.CharField(max_length=512)
    description = models.TextField()

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True

class Text(Card):
    text = models.TextField()
    
    def get_absolute_url(self):
        return reverse('text_card', args=[str(self.id)])

class Media(Card):
    media_locator = models.CharField(max_length=512)

    def get_absolute_url(self):
        return reverse('media_card', args=[str(self.id)])


class Discussion(Card):

    def get_absolute_url(self):
        return reverse('disc_card', args=[str(self.id)])


class Poll(Card):

    def get_absolute_url(self):
        return reverse('poll_card', args=[str(self.id)])


class StackItem(models.Model):
    order = models.IntegerField(default=0)
    stack = models.ForeignKey(Stack, related_name='items')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
