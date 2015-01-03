# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0008_lessondiscussion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessondiscussion',
            name='thread',
            field=models.ForeignKey(related_name='lesson_thread', to='discussions.Post'),
            preserve_default=True,
        ),
    ]
