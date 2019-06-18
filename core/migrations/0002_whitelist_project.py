# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_auto_20190530_0543'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelist',
            name='project',
            field=models.ForeignKey(related_name='membership', to='lessons.Project', null=True),
            preserve_default=True,
        ),
    ]
