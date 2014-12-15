from django.db import models
from django.core.urlresolvers import reverse
# from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

from model_utils.models import TimeStampedModel

from quiz.models import Quiz

CONTENT_TYPES = (
    ('topic', 'Topic'),
    ('reading', 'More To Consider'),
    ('quiz', 'Test Yourself'),
    ('media', 'Consider This'),
)

class Lesson(TimeStampedModel):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.title))
        super(Lesson, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson', args=[str(self.slug)])


class LessonSection(models.Model):
    text = models.TextField()
    content_type = models.CharField(max_length=64, choices=CONTENT_TYPES, default='text')
    lesson = models.ForeignKey(Lesson, related_name='sections')
    
    def get_absolute_url(self):
        return reverse('section', args=[str(self.id)])


class LessonQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='lesson')
    lesson = models.ForeignKey(Lesson, related_name='lesson_quiz')

# class StackItem(models.Model):
#     order = models.IntegerField(default=0)
#     stack = models.ForeignKey(Stack, related_name='items')
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
