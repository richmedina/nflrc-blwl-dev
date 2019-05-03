# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '__first__'),
        ('discussions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LessonDiscussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lesson', models.ForeignKey(related_name='lesson_discussion', to='lessons.Lesson')),
                ('thread', models.ForeignKey(related_name='lesson_post', to='discussions.Post')),
            ],
            options={
                'verbose_name': 'Lesson / Discussion Pair',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LessonModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('lesson', models.ForeignKey(related_name='modules', to='lessons.Lesson')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LessonQuiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lesson', models.ForeignKey(related_name='lesson_quiz', to='lessons.Lesson')),
                ('quiz', models.ForeignKey(related_name='lesson', to='quiz.Quiz')),
            ],
            options={
                'verbose_name': 'Lesson / Quiz Pair',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LessonSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default=b'Coming soon...')),
                ('content_type', models.CharField(default=b'text', max_length=64, choices=[(b'topic', b'Topics'), (b'media', b'Consider This'), (b'reading', b'More To Consider'), (b'quiz', b'Test Yourself'), (b'apply', b'Apply')])),
                ('lesson', models.ForeignKey(related_name='sections', to='lessons.Lesson')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PbllPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512)),
                ('content', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True)),
                ('public', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='module',
            name='project',
            field=models.ForeignKey(related_name='project_modules', to='lessons.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lessonmodule',
            name='module',
            field=models.ForeignKey(related_name='lessons', to='lessons.Module'),
            preserve_default=True,
        ),
    ]
