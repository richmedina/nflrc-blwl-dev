# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0011_pbllpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonsection',
            name='content_type',
            field=models.CharField(default=b'text', max_length=64, choices=[(b'topic', b'Topic'), (b'media', b'Consider This'), (b'reading', b'More To Consider'), (b'quiz', b'Test Yourself'), (b'apply', b'Apply')]),
            preserve_default=True,
        ),
    ]
