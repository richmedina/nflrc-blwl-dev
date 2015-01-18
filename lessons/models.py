from django.db import models
from django.core.urlresolvers import reverse
# from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

from model_utils.models import TimeStampedModel

from quiz.models import Quiz
from discussions.models import Post

CONTENT_TYPES = (
    ('topic', 'Topic'),
    ('media', 'Consider This'),
    ('reading', 'More To Consider'),
    ('quiz', 'Test Yourself'),    
)

class Module(models.Model):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    order = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.title))
        super(Module, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('module', args=[str(self.slug)])   

class Lesson(TimeStampedModel):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    module = models.ForeignKey(Module, related_name='lessons')

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
    
    def __unicode__(self):
        return '%s' % (self.content_type)

    def get_absolute_url(self):
        return reverse('lesson_section', args=[str(self.lesson.slug), str(self.content_type)])


class LessonQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='lesson')
    lesson = models.ForeignKey(Lesson, related_name='lesson_quiz')

    def __unicode__(self):
        return '%s' % (self.quiz)

class LessonDiscussion(models.Model):
    thread = models.ForeignKey(Post, related_name='lesson_post')
    lesson = models.ForeignKey(Lesson, related_name='lesson_discussion')

    def __unicode__(self):
        return '%s -- %s' % (self.lesson, self.thread)

class PbllPage(models.Model):
    title = models.CharField(max_length=512)
    content = models.TextField(blank=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.title))
        super(PbllPage, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pbllpage', args=[str(self.slug)])

# class StackItem(models.Model):
#     order = models.IntegerField(default=0)
#     stack = models.ForeignKey(Stack, related_name='items')
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
