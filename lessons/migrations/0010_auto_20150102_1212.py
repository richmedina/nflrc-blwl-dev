# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0009_auto_20150102_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessondiscussion',
            name='thread',
            field=models.ForeignKey(related_name='lesson_post', to='discussions.Post'),
            preserve_default=True,
        ),
    ]
