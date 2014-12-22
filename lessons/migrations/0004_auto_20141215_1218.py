# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_lessonquiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonquiz',
            name='quiz',
            field=models.ForeignKey(related_name='lesson', to='quiz.Quiz'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lessonsection',
            name='content_type',
            field=models.CharField(default=b'text', max_length=64, choices=[(b'topic', b'Topic'), (b'reading', b'More To Consider'), (b'quiz', b'Test Yourself'), (b'media', b'Consider This')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lessonsection',
            name='lesson',
            field=models.ForeignKey(related_name='sections', to='lessons.Lesson'),
            preserve_default=True,
        ),
    ]
