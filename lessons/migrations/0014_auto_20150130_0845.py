# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0013_auto_20150123_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonsection',
            name='content_type',
            field=models.CharField(default=b'text', max_length=64, choices=[(b'topic', b'Topics'), (b'media', b'Consider This'), (b'reading', b'More To Consider'), (b'quiz', b'Test Yourself'), (b'apply', b'Apply')]),
            preserve_default=True,
        ),
    ]
