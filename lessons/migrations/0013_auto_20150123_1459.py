# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0012_auto_20150121_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lessonsection',
            name='text',
            field=models.TextField(default=b'Coming soon...'),
            preserve_default=True,
        ),
    ]
