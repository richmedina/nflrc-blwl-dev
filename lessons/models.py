from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify

from model_utils.models import TimeStampedModel

from core.models import SiteFile
from quiz.models import Quiz
from discussions.models import Post

CONTENT_TYPES = (
    ('topic', 'Topics'),
    ('media', 'Consider This'),
    ('reading', 'More To Consider'),
    ('quiz', 'Test Yourself'), 
    ('apply', 'Apply'),    
)

class Module(models.Model):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.title))
        super(Module, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('module', args=[str(self.slug)])

    class Meta:
        ordering = ['order']

class Lesson(TimeStampedModel):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    module = models.ForeignKey(Module, related_name='lessons')
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.title))
        super(Lesson, self).save(*args, **kwargs)

        if not self.sections.all():
            section = LessonSection(content_type='topic', lesson=self)
            section.save()
            section = LessonSection(content_type='media', lesson=self)
            section.save()
            section = LessonSection(content_type='reading', lesson=self)
            section.save()
            section = LessonSection(content_type='apply', lesson=self)
            section.save()

        if not self.lesson_discussion.all():
            try:
                user = User.objects.filter(is_superuser=True).get()
                thread = Post(text="Start a discussion!", creator=user, subject=self.title+' Talk', parent_post=None)
                thread.save()
                discussion = LessonDiscussion(thread=thread, lesson=self)
                discussion.save()
            except:
                pass  # Fail silently...

        if not self.lesson_quiz.all():
            try:
                title = '%s %s Quiz'% (self.module.title, self.title)
                quiz = Quiz(title=title, url=title, random_order=False, answers_at_end=True)
                quiz.save()
                lesson_quiz = LessonQuiz(quiz=quiz, lesson=self)
                lesson_quiz.save()
            except Exception as e:
                print e
                # pass  # Fail silently...

    class Meta:
        ordering = ['order']


class LessonSection(models.Model):
    text = models.TextField(default='Coming soon...')
    content_type = models.CharField(max_length=64, choices=CONTENT_TYPES, default='text')
    lesson = models.ForeignKey(Lesson, related_name='sections')
    
    def __unicode__(self):
        return '%s' % (self.content_type)

    def get_absolute_url(self):
        return reverse('lesson_section', args=[str(self.lesson.slug), str(self.content_type)])


class LessonQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='lesson')
    lesson = models.ForeignKey(Lesson, related_name='lesson_quiz')

    class Meta:
        verbose_name = 'Lesson / Quiz Pair'

    def __unicode__(self):
        return '%s --> %s' % (self.lesson, self.quiz)

class LessonDiscussion(models.Model):
    thread = models.ForeignKey(Post, related_name='lesson_post')
    lesson = models.ForeignKey(Lesson, related_name='lesson_discussion')

    class Meta:
        verbose_name = 'Lesson / Discussion Pair'

    def __unicode__(self):
        return '%s --> %s' % (self.lesson, self.thread)

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
