# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_whitelist_honor_agreement'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelist',
            name='participant_type',
            field=models.CharField(default=b'opt1', max_length=8, choices=[(b'opt1', b'Option 1'), (b'opt2', b'Option 2'), (b'staff', b'Staff')]),
            preserve_default=True,
        ),
    ]
