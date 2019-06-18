# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lessondiscussion',
            unique_together=set([('thread', 'lesson')]),
        ),
        migrations.AlterUniqueTogether(
            name='lessonmodule',
            unique_together=set([('module', 'lesson')]),
        ),
    ]
