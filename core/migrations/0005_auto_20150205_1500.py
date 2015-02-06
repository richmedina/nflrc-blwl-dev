# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150204_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whitelist',
            name='email_addr',
            field=models.EmailField(unique=True, max_length=254),
            preserve_default=True,
        ),
    ]
