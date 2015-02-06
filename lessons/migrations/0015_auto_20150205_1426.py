# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0014_auto_20150130_0845'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lessondiscussion',
            options={'verbose_name': 'Lesson / Discussion Pair'},
        ),
        migrations.AlterModelOptions(
            name='lessonquiz',
            options={'verbose_name': 'Lesson / Quiz Pair'},
        ),
    ]
