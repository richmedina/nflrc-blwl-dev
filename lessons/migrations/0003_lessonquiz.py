# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '__first__'),
        ('lessons', '0002_auto_20141212_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonQuiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lesson', models.ForeignKey(related_name='lesson_quiz', to='lessons.Lesson')),
                ('quiz', models.ForeignKey(related_name='quiz', to='quiz.Quiz')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
