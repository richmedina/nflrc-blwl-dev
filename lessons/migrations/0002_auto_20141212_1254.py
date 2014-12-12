# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonsection',
            name='content_type',
            field=models.CharField(default=b'text', max_length=64, choices=[(b'text', b'Text'), (b'media', b'Media (Video/Audio)')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lessonsection',
            name='lesson',
            field=models.ForeignKey(related_name='section', to='lessons.Lesson'),
            preserve_default=True,
        ),
    ]
