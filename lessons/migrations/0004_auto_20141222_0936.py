# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_lessonquiz'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True)),
                ('order', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lesson',
            name='module',
            field=models.ForeignKey(related_name='lessons', default=1, to='lessons.Module'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lessonquiz',
            name='quiz',
            field=models.ForeignKey(related_name='lesson', to='quiz.Quiz'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lessonsection',
            name='content_type',
            field=models.CharField(default=b'text', max_length=64, choices=[(b'topic', b'Topic'), (b'media', b'Consider This'), (b'reading', b'More To Consider'), (b'quiz', b'Test Yourself')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lessonsection',
            name='lesson',
            field=models.ForeignKey(related_name='sections', to='lessons.Lesson'),
            preserve_default=True,
        ),
    ]
