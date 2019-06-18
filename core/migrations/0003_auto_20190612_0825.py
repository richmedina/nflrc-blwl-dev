# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_whitelist_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whitelist',
            name='site_account',
            field=models.ForeignKey(related_name='projects', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
