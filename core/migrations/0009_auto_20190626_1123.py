# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190617_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whitelist',
            name='site_account',
            field=models.ForeignKey(related_name='whitelisting', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
