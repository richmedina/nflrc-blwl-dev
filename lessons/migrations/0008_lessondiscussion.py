# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0002_auto_20150102_1043'),
        ('lessons', '0007_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonDiscussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lesson', models.ForeignKey(related_name='lesson_discussion', to='lessons.Lesson')),
                ('thread', models.ForeignKey(to='discussions.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
