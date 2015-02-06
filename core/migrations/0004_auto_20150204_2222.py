# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_whitelist_participant_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whitelist',
            name='participant_type',
            field=models.CharField(default=b'opt2', max_length=8, choices=[(b'opt1', b'Option 1'), (b'opt2', b'Option 2'), (b'staff', b'Staff')]),
            preserve_default=True,
        ),
    ]
